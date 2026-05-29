import requests
from bs4 import BeautifulSoup
import os

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

URL = "https://playvalorant.com/en-us/news/tags/patch-notes/"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

latest_article = soup.find("a", href=True)

if not latest_article:
    exit()

latest_url = "https://playvalorant.com" + latest_article["href"]

try:
    with open("latest_patch.txt", "r") as f:
        old_url = f.read().strip()
except:
    old_url = ""

if latest_url != old_url:

    payload = {
        "content": f"🚨 New VALORANT Patch Notes!\n{latest_url}"
    }

    requests.post(WEBHOOK_URL, json=payload)

    with open("latest_patch.txt", "w") as f:
        f.write(latest_url)
