import smtplib
from email.mime.text import MIMEText

EMAIL_ADDRESS = "sender@gmail.com" # enter your own email 
EMAIL_PASSWORD = "password" # enter your own 16 character google password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def test_email():
    msg = MIMEText("This is just an email for testing.")
    msg["Subject"] = "Test Email"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = "receiver@gmail.com"  # use your own email for testing

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, "srishravya03@gmail.com", msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Email error: {e}")

test_email()
