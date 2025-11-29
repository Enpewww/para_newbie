import os
from sqlalchemy import create_engine, text

# Connect with OLD password
DATABASE_URL = "postgresql://user:password@127.0.0.1:5433/arthiusaha"

def change_password():
    print(f"Connecting to {DATABASE_URL}...")
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            print("Changing password to '123'...")
            conn.execute(text("ALTER USER \"user\" WITH PASSWORD '123';"))
            conn.commit()
        print("Password changed successfully.")
    except Exception as e:
        print(f"Error changing password: {e}")

if __name__ == "__main__":
    change_password()
