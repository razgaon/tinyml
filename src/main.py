from typing import Dict, List, Optional, Union
from googleapiclient.discovery import Resource
from dotenv import load_dotenv
from src.db import JsonDB
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
    
    user_message: Dict[str, str] = f"""
    Subject: {email_data['subject']}
    To: {email_data['to']}
    From: {email_data['from']}
    Cc: {email_data['cc']}
    Body: {truncated_body}"""

    try:
        completion = call_llm("llama2", user_message, first_name=user_first_name)
        print(completion[:min(10, len(completion))])
        return completion.startswith("True")
    except Exception as e:
        print(f"Failed to evaluate email: {e}")
        return False


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
    total_filtered_emails: int, total_emails_fetched: int
) -> None:
    print(f"Total number of emails fetched:  {total_emails_fetched}")
    print(f"Total number of emails filtered: {total_filtered_emails}")


def main():
    gmail = GmailClient()
    user_first_name = get_user_name()
    filtered_db = JsonDB("src/filtered.json")
    removed_db = JsonDB("src/removed.json")
    all_db = JsonDB("src/all.json")

    page_token: Optional[str] = None

    total_filtered_emails = 0
    total_emails_fetched = 0

    while True:  # Continue looping until no more pages of messages
        # Fetch unread emails
        messages, page_token = gmail.fetch_emails(page_token)

        for message_info in messages:
            
            # Fetch and parse email data
            email_data_parsed = gmail.parse_email_data(message_info)
            
            if "body" not in email_data_parsed:
                continue
            
            total_emails_fetched += 1
            all_db.insert(email_data_parsed)

            # Process email
            # process_email(
                # gmail, message_info, email_data_parsed, user_first_name
            # )
            if (evaluate_email(email_data_parsed, user_first_name)):
                total_filtered_emails += 1
                print("Interesting email: " + email_data_parsed['subject'])
                filtered_db.insert(email_data_parsed)
            else:
                print("Not interesting email: " + email_data_parsed['subject'])
                removed_db.insert(email_data_parsed)
                
        break

        if not page_token:
            break  # Exit the loop if there are no more pages of messages

    report_statistics(total_filtered_emails, total_emails_fetched)


if __name__ == "__main__":
    main()
