import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
Ты — финансовый AI-ассистент для mini app InvestPath AI.

Твоя задача:
- объяснить пользователю, почему выбранный портфель может ему подходить;
- говорить простым, спокойным и понятным языком;
- не обещать доходность;
- не писать, что это индивидуальная инвестиционная рекомендация;
- обязательно напоминать, что это информационно-образовательный сценарий;
- объяснить 3 блока:
  1. Почему этот вариант подходит
  2. Какие сильные стороны у такого портфеля
  3. На что обратить внимание и какие риски есть

Пиши кратко, структурно, без воды.
Максимум 220 слов.
"""

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    user_profile = f"""
Имя: {data.get('name')}
Срок: {data.get('term')}
Сумма: {data.get('amount')}
Цель: {data.get('goal')}
Стиль: {data.get('risk')}
Стратегия: {data.get('strategy')}
Портфель: {data.get('portfolio')}
"""

    response = client.responses.create(
        model="gpt-5.4",
        instructions=SYSTEM_PROMPT,
        input=f"Вот профиль пользователя:\n{user_profile}\n\nСделай персональный разбор этого варианта."
    )

    return jsonify({
        "analysis": response.output_text
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
