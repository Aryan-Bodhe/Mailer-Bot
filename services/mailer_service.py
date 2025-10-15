from socket import gaierror
import yagmail
import pandas as pd

from templates.email_template import EMAIL_TEMPLATE, SUBJECT_TEMPLATE, TEST_EMAIL_BODY, TEST_EMAIL_SUBJECT

class MailerService:
    def __init__(self, sender_email: str, app_password: str):
        """Initialize the Gmail mailer service from environment variables."""
        if not sender_email or not app_password:
            raise ValueError("Missing EMAIL or APP_PASSWORD in .env file")

        self.yag = yagmail.SMTP(sender_email, app_password)

    @staticmethod
    def validate_credentials(email: str, app_pwd: str):
        yag = yagmail.SMTP(email, app_pwd)
        try:
            yag.send(
                to=email,
                subject=TEST_EMAIL_SUBJECT,
                contents=TEST_EMAIL_BODY
            )
            return True
        except Exception as e:
            return False
            
    def get_marks_block(self, marks_dict: dict):
        # Create a neat block like:
        marks_block = "\n".join([f"{exam}: {marks}" for exam, marks in marks_dict.items()])
        return marks_block
    

    def prepare_mail_content(
        self, 
        name: str, 
        course_name: str,
        marks_dict: dict,
        professor_name: str,
        body_template: str = EMAIL_TEMPLATE, 
        subject_template: str = SUBJECT_TEMPLATE
    ):
        exam_name = list(marks_dict.keys())[0]
        if len(marks_dict) > 1:
            exam_name = "All Examinations"

        subject_context = {
            'course_name': course_name,
            'exam_name': exam_name
        }

        body_context = {
            'student_name': name,
            'course_name': course_name,
            'marks_block': self.get_marks_block(marks_dict),
            'professor_name': professor_name
        }

        # Handle these better
        try:
            subject = subject_template.format(**subject_context)
        except Exception as e:
            print('Mail Subject Formatting Failed.')
            subject = "Course Examination Marks"
        
        # Handle these better
        try:
            body = body_template.format(**body_context)
        except Exception as e:
            print('Mail Body Formatting Failed.')
            raise

        return subject, body
    
    def validate_mail_data(
        self, 
        name: str,
        email: str,
    ):
        if not email or pd.isna(email):
            # print(f'❌ Recipient_{i}: {name}, {email}, {marks}.')
            return {
                'Name': name,
                'Email': email,
                'Reason': 'No email address found.'
            }
        
        return None
                
    def send_bulk(
        self, 
        recipient_data: pd.DataFrame, 
        course_name: str,
        professor_name: str,
        body_template: str = EMAIL_TEMPLATE, 
        subject_template: str = SUBJECT_TEMPLATE
    ):
        """
        Send personalized emails.
        """
        # professor_name = os.getenv("PROFESSOR_NAME")
        failed_mails = []
        success = 0

        for i, rec in recipient_data.iterrows():
            name = rec.get("Name")
            email = rec.get("Mail")

            if pd.isna(name):
                name = "Student"


            result = self.validate_mail_data(name, email)

            if result is not None:
                failed_mails.append(result)
                continue

            marks_dict = {
                col: ("NA" if pd.isna(rec[col]) else rec[col])
                for col in recipient_data.columns
                if col not in ['Mail', 'Name']
            }

            subject, body = self.prepare_mail_content(name, course_name, marks_dict, professor_name)

            try:
                # Fill in placeholders dynamically
                self.yag.send(to=email, subject=subject, contents=body)
                success += 1
            
            except gaierror:
                failed_mails.append({
                    'Name': name,
                    'Email': email,
                    'Reason': 'Poor network connection.'
                })
                
            except Exception as e:
                # print(f'❌ Recipient_{i}: {name}, {email}.')
                failed_mails.append({
                    'Name': name,
                    'Email': email,
                    'Reason': 'Internal Mailer Daemon Error (possibly invalid receiver address).'
                })

        return success, len(recipient_data), pd.DataFrame(failed_mails, columns=['Name', 'Email', 'Reason'])