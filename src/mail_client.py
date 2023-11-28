import base64
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
from typing import Dict, List, Optional, Union, Tuple
from googleapiclient.discovery import build, Resource
from google.oauth2.credentials import Credentials
from dataclasses import dataclass


@dataclass
class EmailData:
    subject: str
    to: str
    sender: str
    cc: Optional[str]
    labels: List[str]
    body: str


# If modifying these SCOPES, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


class GmailClient(object):
    def __init__(self):
        self.gmail: Resource = GmailClient._get_gmail_service()

    @staticmethod
    def _get_gmail_service():
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=3001)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return build("gmail", "v1", credentials=creds)

    def fetch_emails(
        self, page_token: Optional[str]
    ) -> Tuple[List[Dict[str, Union[str, List[str]]]], Optional[str]]:
        try:
            results = (
                self.gmail.users()
                .messages()
                .list(
                    userId="me",
                    labelIds=["UNREAD"],
                    pageToken=page_token,  # Include the page token in the request if there is one
                )
                .execute()
            )
        except Exception as e:
            print(f"Failed to fetch emails: {e}")
            return [], None

        messages: List[Dict[str, Union[str, List[str]]]] = results.get("messages", [])
        page_token = results.get("nextPageToken")
        return messages, page_token

    def parse_email_data(
        self, message_info: Dict[str, Union[str, List[str]]]
    ) -> EmailData:
        try:
            msg = (
                self.gmail.users()
                .messages()
                .get(userId="me", id=message_info["id"], format="full")
                .execute()
            )
        except Exception as e:
            print(f"Failed to fetch email data: {e}")
            return {}

        try:
            headers = msg["payload"]["headers"]
            subject = next(
                header["value"] for header in headers if header["name"] == "Subject"
            )
            to = next(header["value"] for header in headers if header["name"] == "To")
            sender = next(
                header["value"] for header in headers if header["name"] == "From"
            )
            cc = next(
                (header["value"] for header in headers if header["name"] == "Cc"), None
            )
        except Exception as e:
            print(f"Failed to parse email data: {e}")
            return {}

        print(f"Fetched email - Subject: {subject}, Sender: {sender}")
        # TODO: Remove junk from the email body (urls)
        # Extract the plain text body
        parts = msg["payload"].get("parts", [])
        for part in parts:
            if part["mimeType"] == "text/plain":
                body = part["body"].get("data", "")
                body = base64.urlsafe_b64decode(body.encode("ASCII")).decode("utf-8")
                break
        else:
            body = ""

        # Parse email data
        email_data_parsed: EmailData = {
            "subject": subject,
            "to": to,
            "from": sender,
            "cc": cc,
            "labels": msg["labelIds"],
            "body": body,
        }
        return email_data_parsed

    def mark_email_as_read(
        self, message_info: Dict[str, Union[str, List[str]]]
    ) -> None:
        try:
            self.gmail.users().messages().modify(
                userId="me", id=message_info["id"], body={"removeLabelIds": ["UNREAD"]}
            ).execute()
            print("Email marked as read successfully")
        except Exception as e:
            print(f"Failed to mark email as read: {e}")
