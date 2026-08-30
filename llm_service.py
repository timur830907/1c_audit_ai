import os
from openai import OpenAI

def generate_audit_explanation(audit_data: dict) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY не установлен в переменной окружения")

    client = OpenAI(api_key=api_key)

    prompt = f"""
    Вы — эксперт по финансовому аудиту и госзакупкам РК.
    Проанализируйте следующую аномальную транзакцию, выявленную алгоритмом XGBoost:
    
    - Идентификаторы документов: {audit_data.get('doc_ids')}
    - БИН поставщика: {audit_data.get('vendor_bin')}
    - Общая сумма: {audit_data.get('total_amount_kzt')} KZT ({audit_data.get('total_amount_mrp')} МРП)
    - Временной интервал между платежами: {audit_data.get('interval_hours')} часов
    - Оценка риска ML: {audit_data.get('risk_score')}
    
    Задачи:
    1. Оцените риск искусственного дробления государственных закупок с целью ухода от открытого конкурса (Закон РК 'О государственных закупках').
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