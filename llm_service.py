import os
from google import genai

def generate_audit_explanation(audit_data: dict) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY не установлен в переменной окружения Render")

    client = genai.Client(api_key=api_key)

    prompt = f"""
    Вы — эксперт по финансовому аудиту и госзакупкам РК.
    Проанализируйте аномальную транзакцию:
    - Документы: {audit_data.get('doc_ids')}
    - БИН поставщика: {audit_data.get('vendor_bin')}
    - Сумма: {audit_data.get('total_amount_kzt')} KZT ({audit_data.get('total_amount_mrp')} МРП)
    - Интервал: {audit_data.get('interval_hours')} ч.
    - Оценка риска ML: {audit_data.get('risk_score')}

    Задачи:
    1. Оцените риск искусственного дробления государственных закупок (Закон РК 'О государственных закупках').
    2. Укажите конкретные статьи законодательства РК, которые могли быть нарушены.
    3. Сформируйте краткое аудиторское заключение с рекомендацией по проверке для бухгалтера/аудитора.
    """

    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt
    )

    return response.text