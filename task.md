# ArthiUsaha - AI Financial Assistant (Amartha x GDG Hackathon)

This project implements the backend and machine learning components for **ArthiUsaha**, an AI-powered financial assistant for MSMEs.

## 📂 Project Structure

*   **`backend/`**: Core FastAPI service, Database Schema (`schema.sql`), and Docker orchestration (`bootstrap.sh`, `compose.yaml`).
*   **`ml_engine/`**: Machine Learning service (Flask) and training notebooks (`model_training.ipynb`).
*   **`HACKATHON_2025_DATA/`**: Raw CSV datasets used for seeding the database.
*   **`scripts/`**: Utility scripts for data loading and management.

## 🚀 Getting Started

### Prerequisites
*   **Docker Desktop** (running with WSL2 backend on Windows).
*   **Python 3.10+**.

### 1. Environment Setup
Navigate to the `backend` directory and start the services (Postgres, n8n, WAHA, Python Runner):

```bash
cd backend
./bootstrap.sh --fresh
```
*   **Postgres**: `localhost:5433` (User: `agent`, Pass: `123`, DB: `amarthafin`)
*   **n8n**: `http://localhost:5678`
*   **WAHA**: `http://localhost:3000`

### 2. Database Seeding
Populate the PostgreSQL database with the provided datasets:

```bash
# Install dependencies if needed
pip install pandas sqlalchemy psycopg2-binary python-dotenv

# Run the loader script
python scripts/load_data.py
```
This script will:
1.  Connect to the Dockerized Postgres (Port 5433).
2.  Truncate existing tables.
3.  Load data from `HACKATHON_2025_DATA/` (handling duplicates automatically).

### 3. Machine Learning
The ML Engine contains models for **Customer Tiering** (Gold/Silver/Bronze).
*   **Training**: Open `ml_engine/model_training.ipynb` to retrain models.
*   **Service**: The ML service runs as a Flask app (containerized).

## 📊 Database Schema
The database `amarthafin` contains the following core tables:
*   `customers`: MSME profiles.
*   `loans`: Loan details and status.
*   `bills`: Repayment schedules and history.
*   `tasks`: Field officer tasks.
*   `task_participants`: Details of task execution (linked to tasks).
*   `agents`: AI Agents configuration.

## ✅ Current Status
*   [x] Database configured and populated.
*   [x] ML Tiering Model trained.
*   [x] WAHA (WhatsApp) integrated via n8n.
*   [x] Project structure cleaned and documented.
