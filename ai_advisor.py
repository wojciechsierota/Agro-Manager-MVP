import os
import json
from google import genai
from dotenv import load_dotenv
from database_manager import DatabaseManager

load_dotenv()
DB_NAME = "agro_manager.db"
HISTORY_FILE = "history.json"
HISTORY_LIMIT = 4
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def get_farm_summary():
    db = DatabaseManager(DB_NAME)
    db.connect()
    operations = db.fetch_all("""
            SELECT 
                Fields.name,
                Operations.task_name,
                Operations.description,
                Operations.date
            FROM Operations
            JOIN Fields ON Operations.field_id = Fields.field_id
        """)
    
    finances = db.fetch_all("""
        SELECT 
            Fields.name, 
            IFNULL((SELECT SUM(cost) FROM Operations WHERE field_id = Fields.field_id), 0),
            IFNULL((SELECT SUM(total_revenue) FROM Sales WHERE field_id = Fields.field_id), 0)
        FROM Fields
    """)
    db.disconnect()
    return f"Past Operations: {operations}. Financial data (Field, Total Costs, Total Revenue): {finances}"


def save_history(history):
    with open(HISTORY_FILE, "w",encoding="utf-8") as f:
        json.dump(history, f, indent = 4, ensure_ascii=False)

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def ask_ai_advisor():
    farm_data = get_farm_summary()
    conversation_history = load_history()

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

            if len(conversation_history) > (HISTORY_LIMIT * 2):
                conversation_history = conversation_history[-(HISTORY_LIMIT * 2):]

            save_history(conversation_history)

        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    ask_ai_advisor()

    # I did fertilization on Field A in March. What is the next logical step?
