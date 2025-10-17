import os
import smtplib
from email.mime.text import MIMEText
import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://dvprogram.state.gov"
KEYWORDS = ["dv-2027", "entries", "open", "registration", "now accepting"]

def send_email(message):
    sender = os.environ["EMAIL_SENDER"]
    receiver = os.environ["EMAIL_RECEIVER"]
    password = os.environ["EMAIL_PASSWORD"]
    subject = os.environ.get("EMAIL_SUBJECT", "DV Lottery Status Update")

    msg = MIMEText(message)
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Email sending failed: {e}")

def check_dv_status():
    print("Checking DV site...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    }
    response = requests.get(URL, headers=headers, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text().lower()

    if any(keyword in text for keyword in KEYWORDS):
        message = f"[{datetime.now()}] 🚀 DV Lottery entries may be open!\nVisit: {URL}"
        print(message)
        send_email(message)
    else:
        print(f"[{datetime.now()}] ❌ Not open yet.")

if __name__ == "__main__":
    check_dv_status()
