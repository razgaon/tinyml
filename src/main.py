from typing import Dict, List, Optional, Union
from googleapiclient.discovery import Resource
from dotenv import load_dotenv
from src.llm import call_llm
from src.mail_client import GmailClient


load_dotenv()


def get_user_name():
    user_first_name = input("Enter your first name: ")
    return user_first_name


def evaluate_email(
    email_data: Dict[str, Union[str, List[str]]],
    user_first_name: str,
) -> bool:
    MAX_EMAIL_LEN = 3000

    truncated_body = email_data["body"][:MAX_EMAIL_LEN] + (
        "..." if len(email_data["body"]) > MAX_EMAIL_LEN else ""
    )
    user_message: Dict[str, str] = {
        "role": "user",
        "content": (
            f"Subject: {email_data['subject']}\n"
            f"To: {email_data['to']}\n"
            f"From: {email_data['from']}\n"
            f"Cc: {email_data['cc']}\n"
            f"Gmail labels: {email_data['labels']}\n"
            f"Body: {truncated_body}"
        ),
    }

    try:
        completion = call_llm("llama2", user_message, first_name=user_first_name)
    except Exception as e:
        print(f"Failed to evaluate email with GPT-4: {e}")
        return False

    # Extract and return the response
    return completion.choices[0].message.content.strip() == "True"


def process_email(
    gmail: Resource,
    message_info: Dict[str, Union[str, List[str]]],
    email_data_parsed: Dict[str, Union[str, List[str]]],
    user_first_name: str,
) -> int:
    # Evaluate email
    if evaluate_email(email_data_parsed, user_first_name):
        print("Email is not worth the time, marking as read")
        gmail.mark_email_as_read(message_info)
        return 1
    else:
        print("Email is worth the time, leaving as unread")
    return 0


def report_statistics(
    total_unread_emails: int, total_pages_fetched: int, total_marked_as_read: int
) -> None:
    print(f"Total number of unread emails fetched: {total_unread_emails}")
    print(f"Total number of pages fetched: {total_pages_fetched}")
    print(f"Total number of emails marked as read: {total_marked_as_read}")
    print(
        f"Final number of unread emails: {total_unread_emails - total_marked_as_read}"
    )


def main():
    gmail = GmailClient()
    user_first_name = get_user_name()

    page_token: Optional[str] = None

    total_unread_emails = 0
    total_pages_fetched = 0
    total_marked_as_read = 0

    while True:  # Continue looping until no more pages of messages
        # Fetch unread emails
        messages, page_token = gmail.fetch_emails(page_token)
        total_pages_fetched += 1
        print(f"Fetched page {total_pages_fetched} of emails")

        total_unread_emails += len(messages)
        for message_info in messages:
            # Fetch and parse email data
            email_data_parsed = gmail.parse_email_data(message_info)

            # Process email
            # total_marked_as_read += process_email(
            #     gmail, message_info, email_data_parsed, user_first_name
            # )
        print(email_data_parsed)
        break

        if not page_token:
            break  # Exit the loop if there are no more pages of messages

    report_statistics(total_unread_emails, total_pages_fetched, total_marked_as_read)


if __name__ == "__main__":
    main()
