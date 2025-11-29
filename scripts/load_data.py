import os
import csv
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load env from backend/.env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'backend', '.env'))

# Get DB URL from env or use default (updated to 5433 for Docker from host)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://agent:123@127.0.0.1:5433/amarthafin")
DATA_DIR = "HACKATHON_2025_DATA"

def truncate_tables(engine):
    """Truncate all tables to ensure clean load without dropping schema."""
    with engine.connect() as conn:
        print("Truncating tables...")
        conn.execute(text("TRUNCATE TABLE customers, loans, bills, tasks, task_participants, agents, workflows, agent_tasks, agent_logs, notifications, msme_profiles, users RESTART IDENTITY CASCADE;"))
        conn.commit()
        print("Tables truncated.")

def load_data():
    print(f"Connecting to {DATABASE_URL}...")
    engine = create_engine(DATABASE_URL)
    
    # Truncate first
    try:
        truncate_tables(engine)
    except Exception as e:
        print(f"Error truncating tables: {e}")
        return

    files_to_load = [
        ("customers.csv", "customers"),
        ("loan_snapshots.csv", "loans"),
        ("bills.csv", "bills"),
        ("tasks.csv", "tasks"),
        ("task_participants.csv", "task_participants"),
        ("dummy_agents.csv", "agents"),
        ("dummy_workflows.csv", "workflows"),
        ("dummy_agent_tasks.csv", "agent_tasks"),
        ("dummy_msme_profiles.csv", "msme_profiles")
    ]

    with engine.connect() as conn:
        for filename, table_name in files_to_load:
            filepath = os.path.join(DATA_DIR, filename)
            if not os.path.exists(filepath):
                print(f"File not found: {filepath}, skipping.")
                continue

            print(f"Loading {filename} into {table_name}...")
            
            try:
                # Tables with potential duplicates that fit in memory
                if table_name in ['customers', 'loans', 'bills', 'tasks', 'agents', 'workflows', 'agent_tasks', 'msme_profiles']:
                    df = pd.read_csv(filepath)
                    
                    # Handle duplicates
                    pk_col = {
                        'customers': 'customer_number',
                        'loans': 'loan_id',
                        'bills': 'bill_id',
                        'tasks': 'task_id',
                        'agents': 'agent_id',
                        'workflows': 'workflow_id',
                        'agent_tasks': 'id',
                        'msme_profiles': 'profile_id'
                    }.get(table_name)
                    
                    if pk_col and pk_col in df.columns:
                        original_len = len(df)
                        df = df.drop_duplicates(subset=[pk_col])
                        if len(df) < original_len:
                            print(f"  Dropped {original_len - len(df)} duplicates from {table_name}")

                    df.to_sql(table_name, engine, if_exists='append', index=False)
                    print(f"Successfully loaded {filename} into {table_name} ({len(df)} rows).")
                
                else:
                    # Large files (task_participants) - use chunking
                    chunksize = 10000
                    for i, chunk in enumerate(pd.read_csv(filepath, chunksize=chunksize)):
                        chunk.to_sql(table_name, engine, if_exists='append', index=False)
                        print(f"  Loaded chunk {i+1} ({len(chunk)} rows)")
                    print(f"Successfully loaded {filename} into {table_name}.")

            except Exception as e:
                print(f"Error loading {table_name}: {e}")

if __name__ == "__main__":
    load_data()
