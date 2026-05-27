"""
ExchangeRate-API Adapter (FREE)
===============================
1500 requests/month on free tier.
To upgrade: replace with OANDA adapter
"""

import requests
from services.base import ForexDataProvider


class ExchangeRateAdapter(ForexDataProvider):

    BASE_URL = "https://api.exchangerate-api.com/v4/latest"

    def get_rate(self, base: str, target: str) -> dict:
        try:
            # Clean symbols
            base = base.replace("/", "").upper()[:3]
            r = requests.get(f"{self.BASE_URL}/{base}", timeout=5)
            data = r.json()
            rate = data["rates"].get(target.upper(), 0)
            return {
                "pair": f"{base}/{target}",
                "rate": round(rate, 4),
                "base": base,
                "target": target,
            }
        except Exception as e:
            return {"pair": f"{base}/{target}", "rate": 0, "error": str(e)}

    def get_all_rates(self, base: str = "USD") -> dict:
        try:
            r = requests.get(f"{self.BASE_URL}/{base}", timeout=5)
            data = r.json()
            important = ["INR", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "SGD", "AED"]
            return {
                "base": base,
                "rates": {k: v for k, v in data["rates"].items() if k in important},
                "last_updated": data.get("time_last_updated"),
            }
        except Exception as e:
            return {"error": str(e)}

    def get_forex_pairs(self, pairs: list) -> list:
        """Takes list of 'USD/INR' format strings, returns rates"""
        result = []
        try:
            # Batch by base currency to minimize API calls
            bases = {}
            for pair in pairs:
                parts = pair.split("/")
                if len(parts) == 2:
                    base, target = parts
                    if base not in bases:
                        bases[base] = []
                    bases[base].append(target)

            for base, targets in bases.items():
                r = requests.get(f"{self.BASE_URL}/{base}", timeout=5)
                if r.status_code == 200:
                    all_rates = r.json().get("rates", {})
                    for target in targets:
                        rate = all_rates.get(target, 0)
                        result.append({
                            "pair": f"{base}/{target}",
                            "rate": round(rate, 4),
                        })
        except Exception as e:
            pass
        return result


# ============================================
# PAID ADAPTER — OANDA (~$50/month)
# Real-time spreads, historical forex data
# ============================================

# import requests, os
# from services.base import ForexDataProvider
#
# class OANDAAdapter(ForexDataProvider):
#
#     BASE_URL = "https://api-fxtrade.oanda.com/v3"
#
#     def __init__(self):
#         self.api_key = os.getenv("OANDA_API_KEY")
#         self.headers = {"Authorization": f"Bearer {self.api_key}"}
#
#     def get_rate(self, base: str, target: str) -> dict:
#         instrument = f"{base}_{target}"
#         r = requests.get(
#             f"{self.BASE_URL}/instruments/{instrument}/candles",
#             headers=self.headers,
#             params={"count": 1, "granularity": "M1"}
#         )
#         # parse response...
