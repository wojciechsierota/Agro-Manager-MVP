import sqlite3
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def get_farm_summary():
    conn = sqlite3.connect('agro_manager.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            Fields.name,
            Operations.task_name,
            Operations.description,
            Operations.date
        FROM Operations
        JOIN Fields ON Operations.field_id = Fields.field_id
    """)
    history = cur.fetchall()
    conn.close()
    return history


def ask_ai_advisor(user_question):

    farm_data = get_farm_summary()
    
    context = f"You are a professional agronomist advisor. Here is the farm history: {farm_data}. "
    full_prompt = context + f"Farmer asks: {user_question}. Answer in English."

    try:
        response = client.models.generate_content(
            model="gemini-flash-lite-latest", 
            contents=full_prompt
        )
        return response.text
    except Exception as e:
        return f"Error details: {e}"


if __name__ == "__main__":
    print("Agro AI Advisor is ready!")
    question = input("Ask your AI Agronomist: ")
    print("\nAnalyzing data...")
    print(ask_ai_advisor(question))

    # I did fertilization on Field A in March. What is the next logical step?
