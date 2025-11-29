import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Try connecting with 'user' and 'password' (default) or '123'
configs = [
    {"user": "user", "password": "password", "db": "postgres"},
    {"user": "user", "password": "123", "db": "arthiusaha"},
    {"user": "agent", "password": "123", "db": "postgres"} # In case already done
]

def fix_docker_db():
    conn = None
    for config in configs:
        try:
            print(f"Trying to connect as {config['user']} with password '{config['password']}'...")
            conn = psycopg2.connect(
                host="127.0.0.1",
                port="5433",
                user=config["user"],
                password=config["password"],
                dbname=config["db"]
            )
            print("Connected successfully!")
            break
        except Exception as e:
            print(f"Failed: {e}")
    
    if not conn:
        print("Could not connect to Docker DB with any known credential.")
        return

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    # 1. Create User 'agent'
    try:
        cur.execute("CREATE USER agent WITH PASSWORD '123';")
        print("User 'agent' created.")
    except psycopg2.errors.DuplicateObject:
        print("User 'agent' already exists.")
        cur.execute("ALTER USER agent WITH PASSWORD '123';")
        print("User 'agent' password updated.")

    # 2. Create Database 'amarthafin'
    try:
        cur.execute("CREATE DATABASE amarthafin OWNER agent;")
        print("Database 'amarthafin' created.")
    except psycopg2.errors.DuplicateDatabase:
        print("Database 'amarthafin' already exists.")

    # 3. Grant privileges
    cur.execute("GRANT ALL PRIVILEGES ON DATABASE amarthafin TO agent;")
    print("Privileges granted.")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    fix_docker_db()
