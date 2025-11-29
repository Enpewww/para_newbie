import csv
import random
import os
from datetime import datetime, timedelta

# Output directory
OUTPUT_DIR = "HACKATHON_2025_DATA"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Constants
NUM_CUSTOMERS = 50
NUM_LOANS = 100
NUM_BILLS = 300
NUM_TASKS = 50
NUM_PARTICIPANTS = 50

# Helper functions
def random_date(start_year=1970, end_year=2000):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))

def random_future_date():
    start = datetime.now()
    end = start + timedelta(days=30)
    return start + timedelta(days=random.randint(0, (end - start).days))

def random_past_date():
    end = datetime.now()
    start = end - timedelta(days=30)
    return start + timedelta(days=random.randint(0, (end - start).days))

# 1. Generate Customers
print("Generating Customers...")
customers = []
for i in range(NUM_CUSTOMERS):
    customer_number = f"CUST-{i+1:05d}"
    customers.append({
        "customer_number": customer_number,
        "date_of_birth": random_date().strftime("%Y-%m-%d"),
        "marital_status": random.choice(["Single", "Married", "Divorced"]),
        "religion": random.randint(1, 5),
        "purpose": random.choice(["Modal Usaha", "Renovasi Rumah", "Pendidikan", "Kesehatan"])
    })

with open(os.path.join(OUTPUT_DIR, "dummy_customers.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=customers[0].keys())
    writer.writeheader()
    writer.writerows(customers)

# 2. Generate Loans
print("Generating Loans...")
loans = []
for i in range(NUM_LOANS):
    loan_id = f"LOAN-{i+1:05d}"
    customer = random.choice(customers)
    principal = random.randint(1000000, 10000000)
    loans.append({
        "loan_id": loan_id,
        "customer_number": customer["customer_number"],
        "principal_amount": principal,
        "outstanding_amount": principal * random.uniform(0.1, 0.9),
        "dpd": random.choice([0, 0, 0, 5, 10, 30])
    })

with open(os.path.join(OUTPUT_DIR, "dummy_loans.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=loans[0].keys())
    writer.writeheader()
    writer.writerows(loans)

# 3. Generate Bills
print("Generating Bills...")
bills = []
for i in range(NUM_BILLS):
    bill_id = f"BILL-{i+1:05d}"
    loan = random.choice(loans)
    amount = loan["principal_amount"] / 10
    bills.append({
        "bill_id": bill_id,
        "loan_id": loan["loan_id"],
        "bill_scheduled_date": random_future_date().strftime("%Y-%m-%d"),
        "bill_paid_date": random_past_date().strftime("%Y-%m-%d") if random.random() > 0.5 else "",
        "amount": amount,
        "paid_amount": amount if random.random() > 0.5 else 0
    })

with open(os.path.join(OUTPUT_DIR, "dummy_bills.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=bills[0].keys())
    writer.writeheader()
    writer.writerows(bills)

# 4. Generate Tasks
print("Generating Tasks...")
tasks = []
for i in range(NUM_TASKS):
    task_id = f"TASK-{i+1:05d}"
    tasks.append({
        "task_id": task_id,
        "task_type": random.choice(["COLLECTION", "SURVEY", "VERIFICATION"]),
        "task_status": random.choice(["PENDING", "IN_PROGRESS", "COMPLETED"]),
        "start_datetime": random_past_date().isoformat(),
        "end_datetime": random_future_date().isoformat(),
        "actual_datetime": random_past_date().isoformat(),
        "latitude": -6.2 + random.uniform(-0.1, 0.1),
        "longitude": 106.8 + random.uniform(-0.1, 0.1),
        "branch_id": f"BRANCH-{random.randint(1, 5):03d}"
    })

with open(os.path.join(OUTPUT_DIR, "dummy_tasks.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=tasks[0].keys())
    writer.writeheader()
    writer.writerows(tasks)

# 5. Generate Task Participants
print("Generating Task Participants...")
participants = []
for i in range(NUM_PARTICIPANTS):
    task = random.choice(tasks)
    loan = random.choice(loans)
    participants.append({
        "task_id": task["task_id"],
        "participant_type": "LOAN",
        "participant_id": loan["loan_id"],
        "is_face_matched": random.choice([True, False]),
        "is_qr_matched": random.choice([True, False]),
        "payment_amount": random.randint(50000, 500000)
    })

with open(os.path.join(OUTPUT_DIR, "dummy_task_participants.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=participants[0].keys())
    writer.writeheader()
    writer.writerows(participants)

# 6. Generate Agents
print("Generating Agents...")
agents = []
roles = ["COLLECTION_AGENT", "VERIFICATION_AGENT", "SALES_AGENT", "SUPPORT_AGENT", "SUPERVISOR_AGENT"]
for i in range(10):
    agents.append({
        "agent_id": i + 1,
        "name": f"Agent-{i+1:03d}",
        "role": random.choice(roles),
        "status": random.choice(["ACTIVE", "IDLE", "BUSY"]),
        "capabilities": "nlp, decision_making, negotiation"
    })

with open(os.path.join(OUTPUT_DIR, "dummy_agents.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=agents[0].keys())
    writer.writeheader()
    writer.writerows(agents)

# 7. Generate Workflows
print("Generating Workflows...")
workflows = []
for i in range(20):
    workflows.append({
        "workflow_id": f"WF-{i+1:03d}",
        "name": f"Workflow {i+1}",
        "description": "Automated process for loan recovery",
        "status": random.choice(["ACTIVE", "PAUSED"])
    })

with open(os.path.join(OUTPUT_DIR, "dummy_workflows.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=workflows[0].keys())
    writer.writeheader()
    writer.writerows(workflows)

# 8. Generate Agent Tasks
print("Generating Agent Tasks...")
agent_tasks = []
for i in range(100):
    agent_tasks.append({
        "agent_id": random.choice(agents)["agent_id"],
        "workflow_id": random.choice(workflows)["workflow_id"],
        "task_type": random.choice(["CALL_CUSTOMER", "VERIFY_DOCS", "SEND_WHATSAPP"]),
        "description": "Perform assigned action",
        "status": random.choice(["PENDING", "IN_PROGRESS", "COMPLETED"]),
        "priority": random.choice(["HIGH", "MEDIUM", "LOW"]),
        "assigned_at": random_past_date().isoformat(),
        "completed_at": random_past_date().isoformat()
    })

with open(os.path.join(OUTPUT_DIR, "dummy_agent_tasks.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=agent_tasks[0].keys())
    writer.writeheader()
    writer.writerows(agent_tasks)

# 9. Generate MSME Profiles
print("Generating MSME Profiles...")
msme_profiles = []
sectors = ["Retail", "Food & Beverage", "Services", "Agriculture", "Manufacturing"]
experience_levels = ["< 1 year", "1-3 years", "3-5 years", "5-10 years", "> 10 years"]
location_types = ["Permanent Shop", "Mobile", "Home-based", "Online Store"]

for customer in customers:
    msme_profiles.append({
        "customer_number": customer["customer_number"],
        "business_name": f"UD {customer['customer_number']} Jaya",
        "business_sector": random.choice(sectors),
        "industry_experience": random.choice(experience_levels),
        "annual_turnover": random.randint(10000000, 500000000),
        "number_of_employees": random.randint(1, 20),
        "location_type": random.choice(location_types)
    })

with open(os.path.join(OUTPUT_DIR, "dummy_msme_profiles.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=msme_profiles[0].keys())
    writer.writeheader()
    writer.writerows(msme_profiles)

print("Dummy data generation complete.")
