import sqlite3
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
DB_NAME = "agro_manager.db"
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def get_farm_summary():
    with sqlite3.connect(DB_NAME) as conn:
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
        return cur.fetchall()


def ask_ai_advisor():
    farm_data = get_farm_summary()
    conversation_history = []

    system_context = (
        f"You are a professional agronomist advisor. "
        f"Here is the farm operation history: {farm_data}. "
        f"Answer in English. Be concise and practical."
    )

    print("\nAgro AI Advisor is ready! (type 'quit' to exit)\n")

    while True:
        user_question = input("Ask your AI Agronomist: ")

        if user_question.lower() == "quit":
            print("Goodbye!")
            break

        conversation_history.append(f"Farmer: {user_question}")
        full_prompt = system_context + "\n" + "\n".join(conversation_history)

        print("\nAnalyzing data...")

        try:
            response = client.models.generate_content(
                model="gemini-flash-lite-latest",
                contents=full_prompt
            )
            answer = response.text
            conversation_history.append(f"Advisor: {answer}")
            print(f"\nAdvisor: {answer}\n")
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    ask_ai_advisor()

    # I did fertilization on Field A in March. What is the next logical step?
