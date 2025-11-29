# Python Backend Setup Guide

This guide will help you set up the Python/Flask backend with PostgreSQL.

## Prerequisites

- Python 3.8 or higher
- PostgreSQL installed and running

## Step 1: Install PostgreSQL

### macOS (using Homebrew)
```bash
brew install postgresql@14
brew services start postgresql@14
```

### Verify PostgreSQL is running
```bash
psql --version
```

## Step 2: Create Database

```bash
# Connect to PostgreSQL
psql postgres

# Create database
CREATE DATABASE arthiusaha;

# Create user (optional, or use default postgres user)
CREATE USER arthiusaha_user WITH PASSWORD 'your_secure_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE arthiusaha TO arthiusaha_user;

# Exit psql
\q
```

## Step 3: Configure Environment Variables

1. Copy the example environment file:
```bash
cd backend
cp .env.example .env
```

2. Edit `.env` and update with your database credentials:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=arthiusaha
DB_USER=postgres
DB_PASSWORD=your_password
```

## Step 4: Install Python Dependencies

```bash
# Make sure you're in the backend directory
cd backend

# Activate your conda environment (you mentioned h8_env)
conda activate h8_env

# Install dependencies
pip install -r requirements.txt
```

## Step 5: Run the Backend

```bash
# Make sure you're in the backend directory
python app.py
```

The server will start on `http://localhost:3000`

## Step 6: Test the API

### Health Check
```bash
curl http://localhost:3000/health
```

### Create a User
```bash
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Test",
    "lastName": "User",
    "phone": "1234567890",
    "customerEmail": "test@example.com",
    "location": "Jakarta",
    "storeName": "Test Store"
  }'
```

### Get All Users
```bash
curl http://localhost:3000/api/users
```

## Troubleshooting

### Connection Error
If you get a connection error, make sure:
1. PostgreSQL is running: `brew services list`
2. Database exists: `psql -l`
3. Credentials in `.env` are correct

### Port Already in Use
If port 3000 is already in use, you can change it in `app.py`:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

## Running Both Frontend and Backend

1. **Terminal 1** - Backend:
```bash
cd backend
conda activate h8_env
python app.py
```

2. **Terminal 2** - Frontend:
```bash
npm run dev
```

Now you can access:
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:3000`
