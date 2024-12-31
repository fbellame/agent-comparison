import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
from markdown import markdown  # Import the markdown library

# Load environment variables
load_dotenv()

def send_email(sender_email: str, receiver_email: str, subject: str, body: str) -> int:
    """
    Send an email using the Gmail SMTP server.

    Input:
        sender_email (str): The sender's email address.
        receiver_email (str): The recipient's email address.
        subject (str): The subject of the email.
        body (str): The body content of the email in Markdown format.

    Return:
        int: Returns 1 if the email is sent successfully.

    Environment Variables:
        GMAIL_PASS_CODE: The application-specific password for the sender's email account.

    Raises:
        Exception: If there is an error during the email sending process.
    """
    # Retrieve the app password from environment variables
    app_password = os.getenv("GMAIL_PASS_CODE")

    if not app_password:
        raise ValueError("Environment variable 'GMAIL_PASS_CODE' is not set")

    # Create the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Convert Markdown to HTML and attach as the email body
    html_body = markdown(body)
    message.attach(MIMEText(html_body, "html"))

    try:
        # Create an SMTP session and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.send_message(message)
        return 1
    except Exception as e:
        raise Exception(f"Failed to send email: {e}")
