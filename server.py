from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

def generate_market_data():
    return {
        "market_trend": random.choice(["рост", "снижение", "боковое движение"]),
        "stocks": random.randint(-2, 3),
        "oil": random.randint(-3, 4),
        "gold": random.randint(-2, 2)
    }

def generate_portfolio_analysis(data):
    risk = random.choice(["низкий", "средний", "умеренно высокий"])
    return_percent = random.randint(6, 15)

    return f"""
📊 Анализ рынка:
Сейчас наблюдается {data['market_trend']} на глобальных рынках.
Акции: {data['stocks']}%
Нефть: {data['oil']}%
Золото: {data['gold']}%

📈 Потенциал:
Ожидаемая доходность: {return_percent}% годовых

⚠️ Риск:
Уровень риска: {risk}

📌 Вывод:
Рынок даёт возможности для сбалансированного инвестирования,
но требует диверсификации и контроля риска.
"""

@app.route("/")
def home():
    return "InvestPath AI backend working"

@app.route("/analyze", methods=["POST"])
def analyze():
    user_data = request.json

    market = generate_market_data()
    analysis = generate_portfolio_analysis(market)

    portfolios = [
        {
            "name": "Базовый рост",
            "stocks": ["Сбер", "Лукойл"],
            "bonds": ["ОФЗ 26212"],
            "funds": ["FXIT"],
            "cash": "10%"
        },
        {
            "name": "Сбалансированный",
            "stocks": ["Норникель", "Сбер"],
            "bonds": ["ОФЗ 26238"],
            "funds": ["TMOS"],
            "cash": "15%"
        }
    ]

    scenarios = {
        "growth": "📈 При росте рынка портфель может показать +10–15%",
        "flat": "➡️ При боковом рынке доход около 5–8%",
        "drop": "📉 При падении возможна просадка до -10%"
    }

    return jsonify({
        "analysis": analysis,
        "portfolios": portfolios,
        "scenarios": scenarios
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
