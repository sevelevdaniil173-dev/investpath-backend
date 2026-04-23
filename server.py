from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

def get_market_context():
    contexts = [
        "Рынок находится в фазе умеренной неопределенности: высокие процентные ставки сдерживают рост акций, но поддерживают доходность облигаций.",
        "Наблюдается постепенное восстановление рынков после волатильного периода, что создаёт возможности для долгосрочных инвесторов.",
        "Текущая макроэкономическая ситуация характеризуется балансом между инфляционным давлением и замедлением роста.",
        "Фондовые рынки демонстрируют смешанную динамику: технологический сектор растёт быстрее, чем защитные активы."
    ]
    return random.choice(contexts)

def get_assets_by_strategy(strategy):
    if "conservative" in strategy:
        return [
            ("ОФЗ (гос. облигации)", "40%"),
            ("Корпоративные облигации", "25%"),
            ("ETF на индекс (S&P 500)", "20%"),
            ("Золото", "10%"),
            ("Кэш", "5%")
        ], "6–10% годовых"
    
    elif "balanced" in strategy:
        return [
            ("ETF S&P 500", "30%"),
            ("ETF на развивающиеся рынки", "15%"),
            ("Облигации", "25%"),
            ("Apple / Microsoft", "15%"),
            ("Золото", "10%"),
            ("Кэш", "5%")
        ], "8–14% годовых"
    
    else:  # aggressive
        return [
            ("Tesla / Nvidia", "30%"),
            ("ETF Nasdaq (технологии)", "25%"),
            ("Крипто (BTC/ETH)", "15%"),
            ("S&P 500", "15%"),
            ("Кэш", "15%")
        ], "12–20% годовых"

def build_analysis(data):
    name = data.get("name", "инвестор")
    term = data.get("term", "средний срок")
    amount = data.get("amount", "не указана")
    goal = data.get("goal", "рост капитала")
    risk = data.get("risk", "сбалансированный")
    strategy = data.get("strategy", "balanced")

    assets, returns = get_assets_by_strategy(strategy)
    market = get_market_context()

    assets_text = "\n".join([f"• {a[0]} — {a[1]}" for a in assets])

    return f"""
Персональный инвестиционный разбор

Профиль:
• Срок: {term}
• Сумма: {amount}
• Цель: {goal}
• Стиль: {risk}

Структура портфеля:
{assets_text}

Анализ рынка:
{market}

Потенциал стратегии:
На выбранном горизонте ({term}) ожидаемый диапазон доходности может составлять {returns}, при условии соблюдения стратегии и диверсификации.

Почему это решение подходит:
Данный портфель сочетает защитные и растущие активы, что позволяет адаптироваться к текущей рыночной ситуации и снижать риски.

Рекомендации:
• инвестировать регулярно (DCA)
• не реагировать на краткосрочные колебания
• пересматривать портфель раз в 3–6 месяцев

Важно:
Материал носит информационно-образовательный характер и не является инвестиционной рекомендацией.
"""

@app.route("/")
def home():
    return "InvestPath backend is running"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json() or {}
    analysis = build_analysis(data)
    return jsonify({"analysis": analysis})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
