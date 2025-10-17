import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://dvprogram.state.gov"
KEYWORDS = ["dv-2027", "entries", "open", "registration", "now accepting"]

def check_dv_status():
    response = requests.get(URL, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text().lower()

    if any(keyword in text for keyword in KEYWORDS):
        print(f"[{datetime.now()}] 🚀 DV Lottery entries may be open!")
    else:
        print(f"[{datetime.now()}] ❌ Not open yet.")

if __name__ == "__main__":
    check_dv_status()
