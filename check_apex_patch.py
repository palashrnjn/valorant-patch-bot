import requests
from bs4 import BeautifulSoup
import os

WEBHOOK_URL = os.getenv("APEX_WEBHOOK")

URL = "https://www.ea.com/games/apex-legends/apex-legends/news?page=1&type=latest"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

article = soup.find("a", href=True)

if not article:
    exit()

href = article["href"]

if not href.startswith("http"):
    latest_url = "https://www.ea.com" + href
else:
    latest_url = href

try:
    with open("latest_apex_patch.txt", "r") as f:
        old_url = f.read().strip()
except:
    old_url = ""

if latest_url != old_url:

    payload = {
        "username": "Apex Legends Updates",
        "content": f"🔥 New Apex Legends Update!\n{latest_url}"
    }

    requests.post(WEBHOOK_URL, json=payload)

    with open("latest_apex_patch.txt", "w") as f:
        f.write(latest_url)
