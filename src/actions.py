from typing import Optional
from src.db import JsonDB
from src.mail_client import GmailClient
from tqdm import tqdm

def collect_emails():
    gmail = GmailClient()
    all_db = JsonDB("src/data/all.json")
    
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

def create_report(filename="report1.md"):
    """
    Generates a markdown report using loops, from a JSON structure containing emails.
    The report includes a date header, followed by the subject of emails and their summaries.

    :param messages: A dictionary with dates as keys and a list of email details as values.
    :return: A string containing the markdown formatted report.
    """
    markdown_report = ""

    summarized_db = JsonDB("src/data/summarized.json")
    messages = summarized_db.read()

    sorted_dates = sorted(messages.keys(), reverse=True)

    for date in tqdm(sorted_dates, desc="Processing Dates"):
        markdown_report += f"## {date}\n\n"

        for email_data_parsed in tqdm(messages[date], desc=f"Emails on {date}"):
            subject = email_data_parsed.get('subject', 'No Subject')
            summary = email_data_parsed['summary']

            markdown_report += f"**Subject:** {subject}\n\n"
            markdown_report += f"**Summary:** {summary}\n\n"
    
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(markdown_report)

    return markdown_report