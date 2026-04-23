from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)


def get_market_context(risk):
    conservative_contexts = [
        "Рынок находится в фазе умеренной неопределённости: высокие ставки поддерживают облигации и защитные инструменты.",
        "На рынке сохраняется осторожный настрой инвесторов, поэтому защитные активы выглядят устойчивее роста.",
        "Текущая макроэкономическая ситуация делает консервативные инструменты более привлекательными для аккуратного входа."
    ]

    balanced_contexts = [
        "Фондовые рынки демонстрируют смешанную динамику: часть секторов растёт, а часть остаётся под давлением.",
        "Рынок постепенно восстанавливается после волатильного периода, что создаёт возможности для сбалансированных решений.",
        "Сейчас заметен баланс между защитными активами и активами роста, что делает умеренные стратегии особенно актуальными."
    ]

    aggressive_contexts = [
        "Технологический и ростовой сегменты рынка остаются более волатильными, но дают повышенный потенциал движения вверх.",
        "На рынке сохраняются условия для активов роста, хотя краткосрочные колебания могут быть довольно резкими.",
        "Агрессивные инструменты остаются чувствительными к новостному фону, но на длинном горизонте способны дать высокий потенциал роста."
    ]

    if risk == "Консервативный":
        return random.choice(conservative_contexts)
    elif risk == "Сбалансированный":
        return random.choice(balanced_contexts)
    else:
        return random.choice(aggressive_contexts)


def get_return_range(risk, term):
    if risk == "Консервативный":
        if "5" in term or "месяц" in term:
            return "6–10% годовых"
        return "7–11% годовых"

    if risk == "Сбалансированный":
        if "5" in term or "месяц" in term:
            return "8–14% годовых"
        return "9–15% годовых"

    if "5" in term or "месяц" in term:
        return "12–20% годовых"
    return "14–22% годовых"


def get_assets(strategy, portfolio):
    conservative_sets = {
        "portfolio_1": [
            ("ОФЗ", "45%"),
            ("Корпоративные облигации", "25%"),
            ("Фонд ликвидности", "20%"),
            ("Золото", "10%"),
        ],
        "portfolio_2": [
            ("ОФЗ", "35%"),
            ("Корпоративные облигации", "25%"),
            ("ETF на индекс S&P 500", "20%"),
            ("Золото", "10%"),
            ("Кэш", "10%"),
        ],
        "portfolio_3": [
            ("ОФЗ", "30%"),
            ("Корпоративные облигации", "25%"),
            ("ETF на индекс", "25%"),
            ("Золото", "10%"),
            ("Кэш", "10%"),
        ],
    }

    balanced_sets = {
        "portfolio_1": [
            ("ETF S&P 500", "35%"),
            ("Облигации", "40%"),
            ("Фонд ликвидности", "25%"),
        ],
        "portfolio_2": [
            ("ETF S&P 500", "30%"),
            ("ETF на развивающиеся рынки", "15%"),
            ("Облигации", "25%"),
            ("Apple / Microsoft", "15%"),
            ("Золото", "10%"),
            ("Кэш", "5%"),
        ],
        "portfolio_3": [
            ("Акции крупных компаний", "30%"),
            ("ETF", "25%"),
            ("Облигации", "25%"),
            ("Золото", "10%"),
            ("Кэш", "10%"),
        ],
    }

    aggressive_sets = {
        "portfolio_1": [
            ("Tesla / Nvidia", "25%"),
            ("ETF Nasdaq", "30%"),
            ("S&P 500", "20%"),
            ("Кэш", "25%"),
        ],
        "portfolio_2": [
            ("Tesla / Nvidia", "30%"),
            ("ETF Nasdaq", "25%"),
            ("Крипто (BTC/ETH)", "15%"),
            ("S&P 500", "15%"),
            ("Кэш", "15%"),
        ],
        "portfolio_3": [
            ("Акции роста", "35%"),
            ("ETF Nasdaq", "25%"),
            ("Крипто (BTC/ETH)", "20%"),
            ("S&P 500", "10%"),
            ("Кэш", "10%"),
        ],
    }

    if "conservative" in strategy:
        return conservative_sets.get(portfolio, conservative_sets["portfolio_2"])
    elif "balanced" in strategy:
        return balanced_sets.get(portfolio, balanced_sets["portfolio_2"])
    else:
        return aggressive_sets.get(portfolio, aggressive_sets["portfolio_2"])


def get_strategy_title(strategy):
    mapping = {
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
    return mapping.get(strategy, strategy)


def get_portfolio_title(portfolio):
    mapping = {
        "portfolio_1": "Портфель 1",
        "portfolio_2": "Портфель 2",
        "portfolio_3": "Портфель 3",
    }
    return mapping.get(portfolio, portfolio)


def build_analysis(data):
    name = data.get("name", "инвестор")
    term = data.get("term", "не указан")
    amount = data.get("amount", "не указана")
    goal = data.get("goal", "не указана")
    risk = data.get("risk", "не указан")
    strategy = data.get("strategy", "")
    portfolio = data.get("portfolio", "")

    strategy_title = get_strategy_title(strategy)
    portfolio_title = get_portfolio_title(portfolio)
    market_context = get_market_context(risk)
    expected_return = get_return_range(risk, term)
    assets = get_assets(strategy, portfolio)

    assets_text = "\n".join([f"• {name_} — {share}" for name_, share in assets])

    if risk == "Консервативный":
        fit_text = (
            "Такой вариант подходит пользователю, которому важно в первую очередь сохранить капитал "
            "и снизить влияние резких рыночных колебаний."
        )
        risk_text = (
            "Главное ограничение такого подхода — более умеренный потенциал роста по сравнению "
            "с более агрессивными стратегиями."
        )
    elif risk == "Сбалансированный":
        fit_text = (
            "Такой портфель выглядит логично для пользователя, которому нужен баланс между ростом "
            "и контролем риска."
        )
        risk_text = (
            "В отдельные периоды возможны просадки, но обычно они мягче, чем у агрессивного подхода."
        )
    else:
        fit_text = (
            "Этот сценарий ближе пользователю, который готов принимать повышенную волатильность "
            "ради более высокого потенциального роста капитала."
        )
        risk_text = (
            "Важно учитывать, что такие решения чувствительнее к новостному фону и рыночным коррекциям."
        )

    return f"""Персональный инвестиционный разбор для {name}

Профиль:
• Срок: {term}
• Сумма: {amount}
• Цель: {goal}
• Стиль: {risk}
• Стратегия: {strategy_title}
• Портфель: {portfolio_title}

Структура портфеля:
{assets_text}

Анализ рынка:
{market_context}

Потенциал стратегии:
На выбранном горизонте ({term}) ожидаемый диапазон доходности может составлять {expected_return}, при условии соблюдения стратегии, диверсификации и спокойного отношения к краткосрочным движениям рынка.

Почему это решение подходит:
{fit_text} С учётом цели «{goal}» и бюджета «{amount}» выбранный подход выглядит как логичный базовый сценарий.

На что обратить внимание:
{risk_text} Кроме того, перед действиями стоит проверить комиссии брокера, минимальные суммы входа и актуальный состав инструментов.

Рекомендации:
• инвестировать поэтапно, а не одной точкой
• пересматривать структуру раз в 3–6 месяцев
• не принимать решения только на эмоциях и новостях

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
    app.run(host="0.0.0.0", port=5001)
.ai-variants-wrap {
  margin-top: 18px;
}

.ai-variants-title {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 12px;
  color: #ffffff;
}

.ai-variant-card {
  background: #0b1220;
  border: 1px solid #22304a;
  border-radius: 14px;
  padding: 14px;
  margin-bottom: 12px;
}

.ai-variant-card h4 {
  margin: 0 0 6px;
  font-size: 17px;
  color: #ffffff;
}

.ai-variant-subtitle {
  color: #94a3b8;
  font-size: 14px;
  margin-bottom: 10px;
}

.ai-variant-list {
  margin: 0;
  padding-left: 18px;
}

.ai-variant-list li {
  margin-bottom: 6px;
  color: #dbe4f0;
  line-height: 1.4;
}

.pro-offer {
  margin-top: 16px;
  padding: 16px;
  background: linear-gradient(180deg, #111827 0%, #0f172a 100%);
  border: 1px solid #334155;
  border-radius: 14px;
}

.pro-offer-title {
  font-size: 17px;
  font-weight: 700;
  margin-bottom: 8px;
  color: #ffffff;
}

.pro-offer-text {
  color: #cbd5e1;
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 12px;
}
