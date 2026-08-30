import os
from openai import OpenAI
from dotenv import load_dotenv
from rag_engine import retrieve_relevant_laws

# Подгружаем переменные из .env
load_dotenv()

def generate_report_from_llm(data: dict) -> str:
    # Инициализируем клиент внутри функции с актуальным API-ключом
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # 1. Сбор контекста и поиск НПА
    anomaly_description = (
        f"Выявлена серия транзакций контрагенту {data['vendor_bin']} "
        f"на общую сумму {data['total_amount_mrp']:.1f} МРП с интервалом {data['interval_hours']:.1f} часов."
    )
    
    relevant_laws = retrieve_relevant_laws(anomaly_description + " дробление 100 МРП")
    laws_context = "\n\n".join([
        f"--- {law['doc_name']}, {law['article']} ---\n{law['text']}"
        for law in relevant_laws
    ])
    
    # 2. Промпты
    system_prompt = (
        "Вы — Высший государственный аудитор Республики Казахстан. "
        "Ваша задача — составить формализованный проект раздела Аудиторского отчета (Акта) "
        "на основе данных ИИ-сканера 1С и выдержек из законодательства РК. "
        "Ответ должен быть строго официальным, содержать описание нарушения, ссылки на НПА РК и рекомендации."
    )

    user_prompt = f"""
ДАННЫЕ АНОМАЛЬНОЙ ОПЕРАЦИИ ИЗ 1С:
- Документ/Серия: {data['doc_ids']}
- БИН Поставщика: {data['vendor_bin']}
- Сумма платежей: {data['total_amount_kzt']:,.2f} KZT ({data['total_amount_mrp']:.1f} МРП)
- Интервал между платежами: {data['interval_hours']:.1f} ч.
- Оценка риска XGBoost: {data['risk_score'] * 100:.1f}%

РЕЛЕВАНТНЫЕ СТАТЬИ НПА РК:
{laws_context}

СФОРМУЛИРУЙТЕ АУДИТОРСКОЕ ЗАКЛЮЧЕНИЕ:
1. Описание факта нарушения (Указать БИН, суммы и схему).
2. Правовая квалификация (Какая статья какого закона РК нарушена).
3. Риски и ответственность (Ссылка на КоАП РК при наличии).
4. Рекомендация аудитора.
"""

    # 3. Вызов API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )
    
    return response.choices[0].message.content