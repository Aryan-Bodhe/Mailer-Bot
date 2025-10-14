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
            print(e)
            return False
            


    def prepare_mail_content(
        self, 
        name: str, 
        marks,
        course_name: str,
        exam_name: str,
        professor_name: str,
        body_template: str = EMAIL_TEMPLATE, 
        subject_template: str = SUBJECT_TEMPLATE
    ):
        subject_context = {
            'course_name': course_name,
            'exam_name': exam_name
        }

        body_context = {
            'student_name': name,
            'course_name': course_name,
            'exam_name': exam_name,
            'marks': marks,
            'professor_name': professor_name
        }

        # Handle these better
        try:
            subject = subject_template.format(**subject_context)
        except Exception as e:
            print('Mail Subject Formatting Failed.')
            raise
        
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
        marks: float
    ):
        if not email or pd.isna(email):
            # email = 'NA'
            # print(f'❌ Recipient_{i}: {name}, {email}, {marks}.')
            return {
                'Name': name,
                'Email': email,
                'Marks': marks,
                'Reason': 'No email address found.'
            }
            

        if not marks or pd.isna(marks):
            # marks = 'NA'
            # print(f'❌ Recipient_{i}: {name}, {email}, {marks}.')
            return {
                'Name': name,
                'Email': email,
                'Marks': marks,
                'Reason': 'No marks found for specified exam.'
            }
        
        return None
                
    def send_bulk(
        self, 
        recipient_data: pd.DataFrame, 
        course_name: str,
        exam_name: str,
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
            marks = rec.get(exam_name)

            if pd.isna(name):
                name = "Student"

            result = self.validate_mail_data(name, email, marks)
            if result is not None:
                failed_mails.append(result)
                continue

            subject, body = self.prepare_mail_content(name, marks, course_name, exam_name, professor_name, body_template, subject_template)

            try:
                # Fill in placeholders dynamically
                self.yag.send(to=email, subject=subject, contents=body)
                # print(f'✅ Recipient_{i}: {name}, {email}, {marks}.')
                success += 1
                
            except Exception as e:
                print(type(e))
                print(f'❌ Recipient_{i}: {name}, {email}, {marks}.')
                failed_mails.append({
                    'Name': name,
                    'Email': email,
                    'Marks': marks,
                    'Reason': 'Internal Mailer Daemon Error (possibly invalid receiver address).'
                })

        return success, len(recipient_data), pd.DataFrame(failed_mails, columns=['Name', 'Email', 'Marks', 'Reason'])