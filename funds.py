import json
from kiteconnect import KiteConnect
from datetime import datetime
import pandas as pd

API_KEY = "83ebjltenz2vhjzo"

# Load access token
with open("access_token.json") as f:
    ACCESS_TOKEN = json.load(f)["access_token"]

kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

try:
    # -----------------------------
    # 💸 Fetch Margins
    # -----------------------------
    margins = kite.margins("equity")

    available = margins.get("available", {})
    utilised = margins.get("utilised", {})

    available_cash = available.get("cash", 0)
    collateral = available.get("collateral", 0)
    adhoc_margin = available.get("adhoc_margin", 0)

    used_margin = utilised.get("debits", 0)
    used_exposure = utilised.get("exposure", 0)

    print("---- 💸 Margin Details ----")
    print(f"Available Cash        : ₹{available_cash:,.2f}")
    print(f"Collateral            : ₹{collateral:,.2f}")
    print(f"Adhoc Margin          : ₹{adhoc_margin:,.2f}")
    print(f"Used Exposure Margin  : ₹{used_exposure:,.2f}")
    print(f"Used Margin           : ₹{used_margin:,.2f}")

    # -----------------------------
    # 📊 Fetch Holdings
    # -----------------------------
    holdings = kite.holdings()

    if holdings:
        df = pd.DataFrame(holdings)
        df["current_value"] = df["quantity"] * df["last_price"]
        total_holdings_value = df["current_value"].sum()
    else:
        total_holdings_value = 0

    print(f"\nTotal Holdings Value  : ₹{total_holdings_value:,.2f}")

    # -----------------------------
    # 🧮 Calculate Net Worth
    # -----------------------------
    net_worth = (
        total_holdings_value
        + available_cash
        + collateral
        + adhoc_margin
        - used_margin
    )

    print("\n=====================================")
    print(f"🪙 TOTAL NET WORTH     : ₹{net_worth:,.2f}")
    print("=====================================")

except Exception as e:
    print("❌ Error fetching account details:", e)


  


