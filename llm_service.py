import os
from google import genai
from rag_engine import search_relevant_context

def generate_audit_explanation(audit_data: dict) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY не установлен в переменной окружения Render")

    client = genai.Client(api_key=api_key)

    risk_score = float(audit_data.get('risk_score', 0.0))
    
    # Извлекаем нормативный контекст через RAG
    legal_context = search_relevant_context(
        query="дробление государственных закупок", 
        risk_score=risk_score
    )

    prompt = f"""
    Вы — эксперт по финансовому аудиту и госзакупкам Республики Казахстан.
    
    НОРМАТИВНАЯ БАЗА РК (Используйте данные статьи для обоснования):
    {legal_context}

    ДАННЫЕ ТРАНЗАКЦИИ ДЛЯ АНАЛИЗА:
    - Документы: {audit_data.get('doc_ids')}
    - БИН поставщика: {audit_data.get('vendor_bin')}
    - Сумма: {audit_data.get('total_amount_kzt')} KZT ({audit_data.get('total_amount_mrp')} МРП)
    - Интервал между актами: {audit_data.get('interval_hours')} ч.
    - Оценка риска ML: {risk_score}

    ЗАДАЧИ:
    1. Оцените риск искусственного дробления государственных закупок.
    2. Сошлитесь на конкретные нормы из предоставленной НОРМАТИВНОЙ БАЗЫ РК.
    3. Сформируйте краткое аудиторское заключение с четкими рекомендациями по проверке.
    """

    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt
    )

    return response.text