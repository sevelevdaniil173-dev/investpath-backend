from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def build_analysis(data):
    name = data.get("name", "пользователь")
    term = data.get("term", "не указан")
    amount = data.get("amount", "не указана")
    goal = data.get("goal", "не указана")
    risk = data.get("risk", "не указан")
    strategy = data.get("strategy", "не выбрана")
    portfolio = data.get("portfolio", "не выбран")

    risk_map = {
        "Консервативный": {
            "fit": "вам важнее сохранить капитал и снизить резкие колебания",
            "strong": "основа такого подхода — облигации, ликвидность и более предсказуемая структура",
            "watch": "доходность обычно ниже, чем у более рискованных решений, особенно на длинной дистанции"
        },
        "Сбалансированный": {
            "fit": "вам важен компромисс между ростом и контролем риска",
            "strong": "портфель сочетает защитные инструменты и активы с потенциалом роста",
            "watch": "в отдельные периоды возможны просадки, но обычно они мягче, чем у агрессивного подхода"
        },
        "Агрессивный": {
            "fit": "вы готовы к более сильным колебаниям ради потенциально более высокого роста",
            "strong": "такая структура лучше подходит для длительного горизонта и активов роста",
            "watch": "просадки могут быть заметными, поэтому важно психологически быть к ним готовым"
        }
    }

    chosen = risk_map.get(risk, {
        "fit": "вы выбрали индивидуальный сценарий",
        "strong": "портфель можно адаптировать под ваш горизонт и цель",
        "watch": "важно следить за рисками и не принимать решения импульсивно"
    })

    portfolio_names = {
        "portfolio_1": "Портфель 1",
        "portfolio_2": "Портфель 2",
        "portfolio_3": "Портфель 3",
    }

    strategy_names = {
        "conservative": "Консервативная стратегия",
        "moderate_conservative": "Умеренно-консервативная стратегия",
        "income_conservative": "Доходная консервативная стратегия",
        "balanced": "Сбалансированная стратегия",
        "growth_balanced": "Стратегия умеренного роста",
        "diversified_balanced": "Диверсифицированная стратегия",
        "aggressive": "Агрессивная стратегия",
        "active_growth": "Стратегия активного роста",
        "high_return": "Высокодоходная стратегия",
    }

    strategy_title = strategy_names.get(strategy, strategy)
    portfolio_title = portfolio_names.get(portfolio, portfolio)

    return f"""Персональный разбор для {name}

Вы выбрали:
• Срок: {term}
• Сумма: {amount}
• Цель: {goal}
• Стиль: {risk}
• Стратегия: {strategy_title}
• Портфель: {portfolio_title}

Почему это может вам подойти:
{chosen["fit"]}. С учётом вашей цели «{goal}» и горизонта «{term}» такой вариант выглядит логично как базовый сценарий.

Сильные стороны:
{chosen["strong"]}. Это помогает сделать подход более структурным и понятным даже на старте.

На что обратить внимание:
{chosen["watch"]}. Кроме того, перед действиями стоит проверить комиссии брокера, минимальные суммы входа и актуальный состав инструментов.

Важно:
Этот материал носит информационно-образовательный характер и не является индивидуальной инвестиционной рекомендацией."""
    

@app.route("/")
def home():
    return "InvestPath backend is running"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json() or {}
    analysis = build_analysis(data)
    return jsonify({"analysis": analysis})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)