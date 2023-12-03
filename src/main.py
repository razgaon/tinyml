from typing import Dict, List, Optional, Union
from dotenv import load_dotenv
from src.db import JsonDB
from src.llm import call_llm
from src.mail_client import GmailClient
from src.templates import get_filter_system_prompt, get_summary_system_prompt


load_dotenv()


def get_user_name():
    user_first_name = input("Enter your first name: ")
    return user_first_name

def get_user_message_in_llm_format(email_data: Dict[str, Union[str, List[str]]]) -> str:
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
    
    return user_message

def summarize_email(
    email_data: Dict[str, Union[str, List[str]]],
    user_first_name: str,
) -> bool:
    
    user_message = get_user_message_in_llm_format(email_data)
    system_prompt = get_summary_system_prompt(user_first_name)
    try:
        completion = call_llm("llama2", system_prompt, user_message, first_name=user_first_name)
        return completion
    except Exception as e:
        print(f"Failed to summarize email: {e}")
        return "Failed to summarize email"

def filter_email(
    email_data: Dict[str, Union[str, List[str]]],
    user_first_name: str,
) -> bool:
    
    user_message = get_user_message_in_llm_format(email_data)
    system_prompt = get_filter_system_prompt(user_first_name)
    try:
        completion = call_llm("llama2", system_prompt, user_message, first_name=user_first_name)
        print(completion[:min(10, len(completion))])
        return completion.startswith("True")
    except Exception as e:
        print(f"Failed to filter email: {e}")
        return False
    
def collect_emails():
    gmail = GmailClient()
    all_db = JsonDB("src/all.json")
    
    page_token: Optional[str] = None

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
            
        if not page_token:
            break 
    print(f"Total number of emails fetched:  {total_emails_fetched}")


def filter_emails():
    user_first_name = get_user_name()
    filtered_db = JsonDB("src/filtered.json")
    removed_db = JsonDB("src/removed.json")
    all_db = JsonDB("src/all.json")

    total_filtered_emails = 0
    total_emails_processed = 0
    
    messages = all_db.read()

    for date in messages:
        for email_data_parsed in messages[date]:        
            total_emails_processed += 1
            all_db.insert(email_data_parsed)

            if (filter_email(email_data_parsed, user_first_name)):
                total_filtered_emails += 1
                print("Interesting email: " + email_data_parsed['subject'])
                filtered_db.insert(email_data_parsed)
            else:
                print("Not interesting email: " + email_data_parsed['subject'])
                removed_db.insert(email_data_parsed)

    print(f"Total number of interesting emails: {total_filtered_emails} / {total_emails_processed}")

def main():
    filter_emails()
    # collect_emails()


if __name__ == "__main__":
    main()
