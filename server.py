from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
import random

app = Flask(__name__)
CORS(app)

def get_market_data():
    try:
        sp500 = yf.Ticker("^GSPC").history(period="1d")
        oil = yf.Ticker("CL=F").history(period="1d")
        gold = yf.Ticker("GC=F").history(period="1d")

        return {
            "sp500": round(sp500["Close"].iloc[-1], 2),
            "oil": round(oil["Close"].iloc[-1], 2),
            "gold": round(gold["Close"].iloc[-1], 2)
        }
    except:
        return {
            "sp500": "н/д",
            "oil": "н/д",
            "gold": "н/д"
        }

def generate_smart_analysis(market):
    trend = random.choice(["рост", "снижение", "нестабильность"])

    return f"""
📊 Рынок сейчас:
S&P 500: {market['sp500']}
Нефть: {market['oil']}
Золото: {market['gold']}

📈 Анализ:
На рынке наблюдается {trend}. 
Движение сырья и индексов указывает на текущую фазу цикла.

📊 Прогноз:
Вероятный диапазон доходности: 7–14% годовых

⚠️ Риски:
Возможна краткосрочная волатильность из-за макроэкономических факторов.
"""

@app.route("/")
def home():
    return "InvestPath AI LEVEL 3"

@app.route("/analyze", methods=["POST"])
def analyze():
    user_data = request.json

    market = get_market_data()
    analysis = generate_smart_analysis(market)

    portfolios = [
        {
            "name": "Рост (агрессивнее)",
            "stocks": ["Сбер", "Лукойл", "Яндекс"],
            "bonds": ["ОФЗ 26212"],
            "funds": ["FXIT"],
            "cash": "5%"
        },
        {
            "name": "Баланс",
            "stocks": ["Норникель", "Сбер"],
            "bonds": ["ОФЗ 26238"],
            "funds": ["TMOS"],
            "cash": "15%"
        }
    ]

    scenarios = {
        "growth": "📈 Рост: портфель может дать 10–15%",
        "flat": "➡️ Боковик: 5–8%",
        "drop": "📉 Падение: -8–12%"
    }

    return jsonify({
        "analysis": analysis,
        "portfolios": portfolios,
        "scenarios": scenarios
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
