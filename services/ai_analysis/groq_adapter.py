"""
Groq AI Adapter (FREE)
======================
Uses LLaMA 3 via Groq for fast AI analysis.
To upgrade: swap to OpenAI or Anthropic adapter
"""

from groq import Groq
from services.base import AIAnalysisProvider
import config
import json


class GroqAdapter(AIAnalysisProvider):

    DISCLAIMER = """
    ⚠️ EDUCATIONAL ONLY: This analysis is AI-generated for educational purposes.
    Not SEBI registered. Not financial advice. Do your own research before investing.
    """

    def __init__(self):
        if config.GROQ_API_KEY:
            self.client = Groq(api_key=config.GROQ_API_KEY)
        else:
            self.client = None

    def _call(self, prompt: str, system: str = None) -> str:
        if not self.client:
            return "⚠️ Add GROQ_API_KEY in .env file to enable AI analysis."
        try:
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.completions.create(
                model="llama3-8b-8192",
                messages=messages,
                max_tokens=800,
                temperature=0.3,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"AI analysis unavailable: {str(e)}"

    def analyze_market(self, market_data: dict, news: list) -> str:
        news_titles = "\n".join([f"- {n['title']}" for n in news[:5]])
        prompt = f"""
        Analyze the current market conditions based on this data:

        MARKET DATA:
        {json.dumps(market_data, indent=2)[:1500]}

        RECENT NEWS:
        {news_titles}

        Provide a concise market analysis covering:
        1. Overall market sentiment (Bullish/Bearish/Neutral)
        2. Key drivers today
        3. Sectors to watch
        4. Key risk factors
        5. Short-term outlook (educational only)

        Keep it under 300 words. Simple language. Indian market focus.
        End with: "This is educational analysis only — not investment advice."
        """
        system = "You are a financial market analyst providing educational market insights. Always remind users this is not financial advice."
        return self.DISCLAIMER + "\n" + self._call(prompt, system)

    def analyze_stock(self, stock_data: dict, news: list) -> str:
        news_titles = "\n".join([f"- {n['title']}" for n in news[:3]])
        prompt = f"""
        Provide an educational analysis of this stock:

        STOCK DATA:
        {json.dumps(stock_data, indent=2)[:1500]}

        RECENT NEWS:
        {news_titles}

        Cover these points:
        1. Business summary (2 lines)
        2. Recent performance analysis
        3. Key financial metrics interpretation
        4. Strengths and concerns
        5. What big investors are doing (if data available)

        Keep it educational. Under 350 words. End with disclaimer.
        """
        system = "You are a stock analyst providing educational analysis. Always note this is for learning purposes only, not investment advice."
        return self.DISCLAIMER + "\n" + self._call(prompt, system)

    def predict_trend(self, historical_data: dict) -> dict:
        """Simple trend direction based on recent price movement"""
        try:
            prices = list(historical_data.get("Close", {}).values())
            if len(prices) < 5:
                return {"direction": "Unknown", "confidence": 0, "reasoning": "Insufficient data"}

            recent = prices[-5:]
            avg_change = (recent[-1] - recent[0]) / recent[0] * 100

            if avg_change > 2:
                direction = "Uptrend"
                confidence = min(abs(avg_change) * 10, 85)
            elif avg_change < -2:
                direction = "Downtrend"
                confidence = min(abs(avg_change) * 10, 85)
            else:
                direction = "Sideways"
                confidence = 50

            return {
                "direction": direction,
                "confidence": round(confidence, 1),
                "reasoning": f"Price moved {avg_change:.2f}% over last 5 periods",
                "disclaimer": "Educational only — not a trading signal",
            }
        except:
            return {"direction": "Unknown", "confidence": 0, "reasoning": "Error calculating trend"}

    def get_investment_suggestion(self, market_data: dict, user_profile: str = "beginner") -> str:
        prompt = f"""
        A {user_profile} investor wants to understand the market.
        Based on current conditions: {json.dumps(market_data, indent=2)[:800]}

        Explain in simple terms:
        1. What is happening in the market right now?
        2. What should a beginner know before investing?
        3. What kind of market environment is this?
        4. Basic principles to follow

        Do NOT suggest specific stocks to buy/sell.
        Keep it educational and beginner-friendly. Under 300 words.
        """
        return self._call(prompt)


# ============================================
# PAID ADAPTER — OpenAI GPT-4 (~$0.01/1k tokens)
# Better analysis quality, longer context
# ============================================

# import openai, os
# from services.base import AIAnalysisProvider
#
# class OpenAIAdapter(AIAnalysisProvider):
#
#     def __init__(self):
#         openai.api_key = os.getenv("OPENAI_API_KEY")
#
#     def _call(self, prompt: str, system: str = None) -> str:
#         messages = []
#         if system:
#             messages.append({"role": "system", "content": system})
#         messages.append({"role": "user", "content": prompt})
#         response = openai.ChatCompletion.create(
#             model="gpt-4-turbo",
#             messages=messages,
#             max_tokens=1000
#         )
#         return response.choices[0].message.content
