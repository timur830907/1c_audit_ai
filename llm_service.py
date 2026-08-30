import os
from openai import OpenAI

def generate_audit_explanation(audit_data: dict) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in environment variables")

    client = OpenAI(api_key=api_key)

    prompt = f"""
    Вы — эксперт по финансовому аудиту и госзакупкам РК.
    Проанализируйте аномальную транзакцию:
    - Документы: {audit_data.get('doc_ids')}
    - БИН поставщика: {audit_data.get('vendor_bin')}
    - Сумма: {audit_data.get('total_amount_kzt')} KZT ({audit_data.get('total_amount_mrp')} МРП)
    - Интервал между платежами: {audit_data.get('interval_hours')} ч.
    - Оценка риска (ML): {audit_data.get('risk_score')}

    Задачи:
    1. Оцените риск искусственного дробления государственных закупок с целью ухода от открытого конкурса.
    2. Укажите конкретные статьи законодательства РК, которые могли быть нарушены.
    3. Сформируйте краткое и четкое аудиторское заключение с рекомендацией по проверке для бухгалтера/аудитора.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Вы — эксперт по финансовому аудиту и госзакупкам РК."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content