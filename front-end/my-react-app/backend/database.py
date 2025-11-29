import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

def get_connection():
    """Create and return a database connection."""
    try:
        conn = psycopg2.connect(**Config.get_db_config())
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        raise

def init_db():
    """Initialize the database and create tables if they don't exist."""
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Create users table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                firstName VARCHAR(100),
                lastName VARCHAR(100),
                phone VARCHAR(20),
                customerEmail VARCHAR(255),
                location VARCHAR(255),
                storeName VARCHAR(255),
                latitude DECIMAL(10, 8),
                longitude DECIMAL(11, 8),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Add columns if they don't exist (for existing tables)
        cur.execute("""
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='users' AND column_name='latitude') THEN
                    ALTER TABLE users ADD COLUMN latitude DECIMAL(10, 8);
                END IF;
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='users' AND column_name='longitude') THEN
                    ALTER TABLE users ADD COLUMN longitude DECIMAL(11, 8);
                END IF;
            END $$;
        """)
        
        conn.commit()
        print("Database initialized successfully")
        
    except psycopg2.Error as e:
        print(f"Error initializing database: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            cur.close()
            conn.close()

def create_user(user_data):
    """Insert a new user into the database."""
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO users (firstName, lastName, phone, customerEmail, location, storeName, latitude, longitude)
            VALUES (%(firstName)s, %(lastName)s, %(phone)s, %(customerEmail)s, %(location)s, %(storeName)s, %(latitude)s, %(longitude)s)
            RETURNING id
        """, user_data)
        
        user_id = cur.fetchone()[0]
        conn.commit()
        return user_id
        
    except psycopg2.Error as e:
        print(f"Error creating user: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            cur.close()
            conn.close()

def check_user_exists(phone):
    """Check if a user with the given phone already exists."""
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT id, firstName, lastName, phone, customerEmail, location, storeName, created_at
            FROM users
            WHERE phone = %s
            LIMIT 1
        """, (phone,))
        
        user = cur.fetchone()
        return user
        
    except psycopg2.Error as e:
        print(f"Error checking user existence: {e}")
        raise
    finally:
        if conn:
            cur.close()
            conn.close()

def get_all_users():
    """Retrieve all users from the database."""
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT id, firstName, lastName, phone, customerEmail, location, storeName, created_at
            FROM users
            ORDER BY created_at DESC
        """)
        
        users = cur.fetchall()
        return users
        
    except psycopg2.Error as e:
        print(f"Error fetching users: {e}")
        raise
    finally:
        if conn:
            cur.close()
            conn.close()
