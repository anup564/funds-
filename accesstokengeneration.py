import json
import pyotp
from urllib.parse import urlparse, parse_qs
from playwright.sync_api import sync_playwright
from kiteconnect import KiteConnect
import time

with open("credentials.json") as f:
    c = json.load(f)

USER_ID = c["user_id"]
PASSWORD = c["password"]
TOTP_SECRET = c["totp_secret"]
API_KEY = c["api_key"]
API_SECRET = c["api_secret"]

totp = pyotp.TOTP(TOTP_SECRET).now()
kite = KiteConnect(api_key=API_KEY)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto(f"https://kite.zerodha.com/connect/login?v=3&api_key={API_KEY}")

    page.fill("#userid", USER_ID)
    page.fill("#password", PASSWORD)
    page.click('button[type="submit"]')

    page.wait_for_timeout(2000)
    page.fill('input[type="number"]', totp)

    # ✅ WAIT UNTIL request_token APPEARS
    page.wait_for_function(
        "() => window.location.href.includes('request_token=')",
        timeout=60000
    )

    redirect_url = page.url
    browser.close()

parsed = urlparse(redirect_url)
request_token = parse_qs(parsed.query)["request_token"][0]

session = kite.generate_session(request_token, API_SECRET)
access_token = session["access_token"]

with open("access_token.json", "w") as f:
    json.dump(
        {
            "access_token": access_token,
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        f,
        indent=2
    )

print("✅ ACCESS TOKEN GENERATED SUCCESSFULLY")
print("Saved in access_token.json")
