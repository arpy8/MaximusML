import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

smtp_port = 587
smtp_server = "smtp.gmail.com"
username = os.environ.get("GMAIL_USERNAME")
password = os.environ.get("GMAIL_PASSWORD")


def send_welcome(email, name):
    if username is None or password is None:
        print("Error: SMTP credentials are not set.")
        return

    msg = MIMEMultipart()
    msg["From"] = username
    msg["To"] = email
    msg["Subject"] = "Welcome to our platform!"

    body = f"Dear {name},\n\nWelcome to our platform! We are excited to have you on board.\n\nPlease let us know if you have any questions or need assistance.\n\nBest regards,\nThe Platform Team"
    msg.attach(MIMEText(body, "plain"))

    server = None
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection

        # Login to the SMTP server
        # server.login(username, password)
        server.login(username, password)

        server.sendmail(username, email, msg.as_string())

        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")

    finally:
        if server is not None:
            server.quit()
