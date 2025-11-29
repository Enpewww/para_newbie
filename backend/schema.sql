-- Enable UUID extension if needed (though IDs seem to be strings/hashes)
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Customers Table
CREATE TABLE customers (
    customer_number VARCHAR(255) PRIMARY KEY,
    date_of_birth DATE,
    marital_status VARCHAR(50),
    religion INTEGER,
    purpose TEXT
);

-- 2. Loans Table (from loan_snapshots)
-- Note: loan_snapshots seems to be a snapshot, but we'll treat it as the master loan record for now.
CREATE TABLE loans (
    loan_id VARCHAR(255) PRIMARY KEY,
    customer_number VARCHAR(255) REFERENCES customers(customer_number),
    principal_amount DECIMAL(15, 2),
    outstanding_amount DECIMAL(15, 2),
    dpd INTEGER
);

-- 3. Bills Table
CREATE TABLE bills (
    bill_id VARCHAR(255) PRIMARY KEY,
    loan_id VARCHAR(255) REFERENCES loans(loan_id),
    bill_scheduled_date DATE,
    bill_paid_date DATE,
    amount DECIMAL(15, 2),
    paid_amount DECIMAL(15, 2)
);

-- 4. Tasks Table
CREATE TABLE tasks (
    task_id VARCHAR(255) PRIMARY KEY,
    task_type VARCHAR(50),
    task_status VARCHAR(50),
    start_datetime TIMESTAMP,
    end_datetime TIMESTAMP,
    actual_datetime TIMESTAMP,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    branch_id VARCHAR(255)
);

-- 5. Task Participants Table
-- participant_id is polymorphic (can be loan_id, customer_id, etc.), but data suggests 'LOAN'.
-- We will index it but maybe not enforce FK strictly if types vary, 
-- though profiling showed 'LOAN' type, so we can try linking to loans.
CREATE TABLE task_participants (
    id SERIAL PRIMARY KEY,
    task_id VARCHAR(255), -- REFERENCES tasks(task_id), -- Logical relationship (Note: Data may contain orphans)
    participant_type VARCHAR(50),
    participant_id VARCHAR(255), -- Logically references loans(loan_id) if type='LOAN'
    is_face_matched BOOLEAN,
    is_qr_matched BOOLEAN,
    payment_amount DECIMAL(15, 2)
);

-- Indexes for performance
CREATE INDEX idx_loans_customer ON loans(customer_number);
CREATE INDEX idx_bills_loan ON bills(loan_id);
CREATE INDEX idx_task_participants_task ON task_participants(task_id);

-- 6. Users Table (from my-react-app)
CREATE TABLE users (
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
);

-- 7. Agents Table (Multi-Agent System)
CREATE TABLE agents (
    agent_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    role VARCHAR(50), -- e.g., 'COLLECTION', 'VERIFICATION', 'SALES'
    status VARCHAR(50), -- 'ACTIVE', 'IDLE', 'BUSY'
    capabilities TEXT, -- JSON or comma-separated list of skills
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. Workflows Table
CREATE TABLE workflows (
    workflow_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    status VARCHAR(50), -- 'ACTIVE', 'PAUSED'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. Agent Tasks (Specific assignments)
CREATE TABLE agent_tasks (
    id SERIAL PRIMARY KEY,
    agent_id INTEGER REFERENCES agents(agent_id),
    workflow_id VARCHAR(255) REFERENCES workflows(workflow_id),
    task_type VARCHAR(50),
    description TEXT,
    status VARCHAR(50), -- 'PENDING', 'IN_PROGRESS', 'COMPLETED', 'FAILED'
    priority VARCHAR(20), -- 'HIGH', 'MEDIUM', 'LOW'
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- 10. Agent Logs (Audit trail)
CREATE TABLE agent_logs (
    id SERIAL PRIMARY KEY,
    agent_id INTEGER REFERENCES agents(agent_id),
    action VARCHAR(100),
    details TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 11. Notifications
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    recipient_type VARCHAR(50), -- 'AGENT', 'SYSTEM', 'USER'
    recipient_id VARCHAR(255),
    title VARCHAR(100),
    message TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 12. MSME Profiles (Enriched Data)
CREATE TABLE msme_profiles (
    profile_id SERIAL PRIMARY KEY,
    customer_number VARCHAR(255),
    business_name VARCHAR(255),
    business_sector VARCHAR(100),
    industry_experience VARCHAR(50),
    annual_turnover DECIMAL(15, 2),
    number_of_employees INTEGER,
    location_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_msme_customer FOREIGN KEY (customer_number) REFERENCES customers(customer_number)
);

-- Indexes
CREATE INDEX idx_agent_tasks_agent ON agent_tasks(agent_id);
CREATE INDEX idx_agent_logs_agent ON agent_logs(agent_id);
CREATE INDEX idx_msme_profiles_customer ON msme_profiles(customer_number);
