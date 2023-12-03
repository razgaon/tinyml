from src.actions import create_report
from src.processing import filter_emails, summarize_emails

def main():
    # Optional: collect fresh emails from gmail.
    # collect_emails()
    
    # summarize_emails()
    # filter_emails()
    create_report()
    
    


if __name__ == "__main__":
    main()
