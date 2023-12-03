def get_system_prompt(first_name):
    return """My name is {first_name}, and your task is to assist in filtering my Email inbox. 
            
            Criteria for an interesting email:
            1. A speaker event that focuses on AI or computer science topics.
            
            You need to distinguish between promotional, automated, or mass-sent emails and personal communications.\n\n
            
            Criteria for Ignoring an Email:\n
            - Dancing groups, singing groups, or other performance groups
            
            The user message you will receive will have the following format:\n
            Subject: <email subject>\n
            To: <to names, to emails>\n
            From: <from name, from email>\n
            Cc: <cc names, cc emails>\n
            Gmail labels: <labels>\n
            Body: <plaintext body of the email>\n\n
            
            Respond with True if the email is interesting, otherwise False.
            
            Your response must be either True or False. Do not include any other text in your response.\n\n"""
