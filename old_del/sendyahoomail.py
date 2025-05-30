import smtplib
from email.mime.text import MIMEText

# Yahoo SMTP server details
SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 587
USERNAME = "prasannap731@yahoo.in"  # Replace with your Yahoo email
PASSWORD = "njgjglaneifiozlf"  # Use an App Password, not your regular password

def send_email(to_email, subject, message):
    """Send an email using Yahoo SMTP."""
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = USERNAME
    msg["To"] = to_email

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(USERNAME, PASSWORD)
        server.sendmail(USERNAME, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Example usage Recipient email.
send_email("prasannap731@yahoo.in", "Test Email", "Hello, this is a test email from Python!")
