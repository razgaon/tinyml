def get_filter_system_prompt(first_name):
    return f"""My name is {first_name}, and your task is to assist in filtering my Email inbox. 
            
            Criteria for an interesting email:
            1. A speaker event that focuses on AI or computer science topics.
            
            You need to distinguish between promotional, automated, or mass-sent emails and personal communications.\n\n
            
            Criteria for Ignoring an Email:\n
            - Dancing groups, singing groups, or other performance groups
            
            Respond with True if the email is interesting, otherwise False.
            
            Your response must be either True or False. Do not include any other text in your response.\n\n"""

def get_summary_system_prompt(first_name):
    return f"""My name is {first_name}, and your task is to assist in summarizing emails for me. 
            
            Please summarize the following email, ensuring that the key message and essential details are retained while omitting any unnecessary information. 
            The summary should be concise, clear, and accurately reflect the main points and intent of the email. It should be about 3-5 sentences long.\n\n
            
            The user message you will receive will have the following format:\n
            Subject: <email subject>\n
            To: <to names, to emails>\n
            From: <from name, from email>\n
            Body: <plaintext body of the email>\n\n
            
            Example:
            Subject: Re: [Next Social] Next House Laser Tag Night!!\n
            To: next-forum <next-forum@mit.edu>\n
            From: Next Social <next-social@mit.edu>\n
            Body: We have ~10 leftover slots. If you wanna play laser tag tonight (all paid\r\nfor, including the Uber with reimbursement), COME ON DOWN!!!\r\nOn Sat, Dec 2, 2023, 7:12 PM Next Social <next-social@mit.edu> wrote:\r\n> Happening now! If you got a slot (or want to try to snag one) come to TFL\r\n> right now!! We are doing headcount and assembling into Ubers, so go go go\r\n> go goooo\r\n>\r\n> On Sat, Dec 2, 2023, 4:51 PM Next Social <next-social@mit.edu> wrote:\r\n>\r\n>> Heyo Nexties,\r\n>>\r\n>> Reminder that this is happening tonight! Those of you who have been\r\n>> selected to go laser tagging should have been emailed earlier this\r\n>> afternoon that you got a spot (very sorry for late notice). To those others\r\n>> who still wish to go, you can show up to the TFL at 7:15pm for a chance to\r\n>> go in case people don't show up. All 44 people will *definitely not*\r\n>> show up, so if you're at all interested and didn't get a spot or forgot to\r\n>> fill out the form, please come on down!!\r\n>>\r\n>> If you would like to attend another outing event similar to this in the\r\n>> near future, we've made an interest form you can fill out here (should\r\n>> take like 1min I swear):\r\n>> \r\n>>\r\n>> Grazie,\r\n>> *yfn Next Social Comm*\r\n>>\r\n>> On Mon, Nov 27, 2023 at 9:40PM Next Social <next-social@mit.edu> wrote:\r\n>>\r\n>>> Greetings Next House,\r\n>>>\r\n>>> Do you like lasers? Wouldst thou like to shoot thy fellow Nexties with\r\n>>> lasers? Sign up for *Next House Laser Tag* happening *this Saturday,\r\n>>> December 2nd*!!!\r\n>>>\r\n>>> Sign up here:\r\n>>> \r\n>>>\r\n>>> There are only 44 spots available, and it is first come, first served.\r\n>>> So sign up soon!\r\n>>>\r\n>>> sincerely,\r\n>>> *yfn Next Social Comm*\r\n>>>\r\n>>\r\n\n
            
            Response:
            Next Social has announced that there are approximately 10 remaining slots for tonight's laser tag event. Participation is fully funded, including reimbursed Uber rides. Interested individuals who didn't secure a spot earlier are encouraged to arrive at TFL immediately for a chance to join. The email also mentions a future outing and provides a link to an interest form for those who wish to participate in similar events.
            
            
            Only provide the summary, do not include any other text in your response.\n\n
            """