import os
import time
from sqlalchemy import create_engine, text

from dotenv import load_dotenv

load_dotenv()

# Get DB URL from env or use default
DATABASE_URL = os.getenv("DATABASE_URL")

def init_db():
    print(f"Connecting to {DATABASE_URL}...")
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            # Drop tables to ensure schema is enforced
            print("Dropping existing tables...")
            conn.execute(text("DROP TABLE IF EXISTS msme_profiles, agent_logs, agent_tasks, notifications, task_participants, tasks, bills, loans, customers, users, agents, workflows CASCADE;"))
            conn.commit()
            
            print("Creating tables from schema.sql...")
            with open("backend/schema.sql", "r") as f:
                schema = f.read()
                conn.execute(text(schema))
                conn.commit()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise e

if __name__ == "__main__":
    # Retry logic in case DB is starting up
    for i in range(5):
        try:
            init_db()
            break
        except Exception as e:
            print(f"Retrying in 2 seconds... Error: {e}")
            time.sleep(2)
