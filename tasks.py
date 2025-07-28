import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

MY_EMAIL = os.environ.get("EMAIL")
MY_PASSWORD = os.environ.get("GMAIL_PASSWORD")  # Load from env in real apps

def send_email(subject, body, to_email):
    msg = MIMEMultipart()
    msg["From"] = MY_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(MY_EMAIL, MY_PASSWORD)
        server.sendmail(MY_EMAIL, to_email, msg.as_string())
        server.quit()
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def send_registration_email(username, email):
    print(f"📧 Sending registration email to: {username}, {email}", flush=True)
    send_email(
        to_email=email,
        subject="Hi there! You Successfully signed up.",
        body=f"Hi {username}, you have successfully registered to the Stores REST API!",
    )