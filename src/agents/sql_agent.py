import os
import sqlite3
from pathlib import Path
import sys

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.project_paths import advanced_data_path


load_dotenv()

DB_PATH = advanced_data_path("telemetry.db")
SAFE_SQL_PREFIXES = ("select", "with")


def get_schema():
    return """
    Table: scored_users
    Columns: user_id (INT), days_since_last_activity (INT), engagement_velocity (FLOAT, ratio of events in last 14 days vs prior 14 days), frustration_index (INT, formula based on quiz fails and rage clicks), completion_ratio (FLOAT), total_events (INT), mrr (INT, monthly recurring revenue), churned (INT 0/1), risk_score (FLOAT 0-1), primary_churn_driver (TEXT)
    """


def sanitize_sql_query(query: str) -> str:
    cleaned = query.strip().strip("`")
    cleaned = cleaned.replace("```sql", "").replace("```", "").strip()

    if not cleaned:
        raise ValueError("The agent returned an empty SQL query.")

    normalized = cleaned.lower()
    if not normalized.startswith(SAFE_SQL_PREFIXES):
        raise ValueError("Only SELECT queries are allowed.")

    if ";" in cleaned.rstrip(";"):
        raise ValueError("Multiple SQL statements are not allowed.")

    return cleaned.rstrip(";")


def run_sql(query: str):
    if not DB_PATH.exists():
        return f"SQL Error: Database not found at {DB_PATH}"

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            columns = [description[0] for description in (cursor.description or [])]

        if not results:
            return "No results found."

        lines = [" | ".join(columns)]
        lines.extend(" | ".join(str(item) for item in row) for row in results)
        return "\n".join(lines)
    except Exception as exc:
        return f"SQL Error: {exc}"


def ask_agent(question):
    """
    Translate natural language to SQL, execute it, and summarize the result.
    """
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key or api_key == "your_groq_api_key_here":
        return (
            "Agent offline: `GROQ_API_KEY` is not configured in `.env`. "
            "The autonomous SQL assistant needs an LLM connection to translate English into SQL."
        )

    try:
        from groq import Groq

        client = Groq(api_key=api_key)

        prompt_sql = f"""
        You are a senior data engineer. Write a SQL query for SQLite based on this schema:
        {get_schema()}

        Question: {question}

        Return only a single SELECT query with at most 10 rows.
        """

        comp_sql = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt_sql}],
            temperature=0.0,
        )
        sql_query = sanitize_sql_query(comp_sql.choices[0].message.content)

        raw_data = run_sql(sql_query)
        if "SQL Error" in raw_data:
            return f"The agent tried to run:\n`{sql_query}`\n\nBut hit an error:\n{raw_data}"

        prompt_ans = f"""
        You are a strategic AI advisor. The user asked: "{question}"
        The database returned this raw data:
        {raw_data}

        Summarize the data into a concise, actionable business insight.
        """

        comp_ans = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt_ans}],
            temperature=0.7,
        )

        final_answer = comp_ans.choices[0].message.content
        return f"**Executed SQL:**\n```sql\n{sql_query}\n```\n\n**Agent Insight:**\n{final_answer}"
    except Exception as exc:
        return f"Agent Error: {exc}"


if __name__ == "__main__":
    print(ask_agent("What is the average risk score for users with a frustration index higher than 5?"))
