import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# DB Config
DB_CONFIG = {
    "host": "127.0.0.1",
    "port": "5433",
    "user": "agent",
    "password": "123",
    "database": "amarthafin"
}

def get_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return conn

def apply_schema():
    conn = get_connection()
    cur = conn.cursor()

    print("1. Creating n8n_chat_histories table...")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS n8n_chat_histories (
            id SERIAL PRIMARY KEY,
            session_id VARCHAR(255) NOT NULL,
            message JSONB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_n8n_chat_histories_session ON n8n_chat_histories(session_id);
    """)

    print("2. Adding Semantic Comments (Descriptions)...")
    comments = [
        # Customers
        "COMMENT ON TABLE customers IS 'Master data of MSME customers (Mitra Amartha).';",
        "COMMENT ON COLUMN customers.customer_number IS 'Unique identifier for the customer (e.g., CUST-00001).';",
        "COMMENT ON COLUMN customers.date_of_birth IS 'Customer birth date.';",
        "COMMENT ON COLUMN customers.marital_status IS 'Marital status (MARRIED, SINGLE, etc.).';",
        "COMMENT ON COLUMN customers.religion IS 'Religion code.';",
        "COMMENT ON COLUMN customers.purpose IS 'Purpose of joining or loan purpose.';",

        # Loans
        "COMMENT ON TABLE loans IS 'Loan portfolio data for customers.';",
        "COMMENT ON COLUMN loans.loan_id IS 'Unique identifier for the loan.';",
        "COMMENT ON COLUMN loans.customer_number IS 'Reference to the customer.';",
        "COMMENT ON COLUMN loans.principal_amount IS 'Total principal amount of the loan.';",
        "COMMENT ON COLUMN loans.outstanding_amount IS 'Remaining amount to be paid.';",
        "COMMENT ON COLUMN loans.dpd IS 'Days Past Due (0 = Current, >0 = Late).';",

        # Bills
        "COMMENT ON TABLE bills IS 'Repayment schedules and transaction history.';",
        "COMMENT ON COLUMN bills.bill_id IS 'Unique identifier for the bill/installment.';",
        "COMMENT ON COLUMN bills.loan_id IS 'Reference to the loan.';",
        "COMMENT ON COLUMN bills.bill_scheduled_date IS 'Due date for the payment.';",
        "COMMENT ON COLUMN bills.bill_paid_date IS 'Actual date when payment was received (NULL if unpaid).';",
        "COMMENT ON COLUMN bills.amount IS 'Installment amount due.';",
        "COMMENT ON COLUMN bills.paid_amount IS 'Amount actually paid.';",

        # Tasks
        "COMMENT ON TABLE tasks IS 'Field tasks assigned to officers (Business Partners).';",
        "COMMENT ON COLUMN tasks.task_id IS 'Unique identifier for the field task.';",
        "COMMENT ON COLUMN tasks.task_type IS 'Type of task (e.g., COLLECTION, VERIFICATION).';",
        "COMMENT ON COLUMN tasks.task_status IS 'Status of the task (e.g., DONE, PENDING).';",
        "COMMENT ON COLUMN tasks.start_datetime IS 'Scheduled start time.';",
        "COMMENT ON COLUMN tasks.actual_datetime IS 'Actual execution time.';",
        "COMMENT ON COLUMN tasks.latitude IS 'GPS Latitude of task location.';",
        "COMMENT ON COLUMN tasks.longitude IS 'GPS Longitude of task location.';",

        # Task Participants
        "COMMENT ON TABLE task_participants IS 'Details of participants/items involved in a task (e.g., specific loans collected).';",
        "COMMENT ON COLUMN task_participants.task_id IS 'Reference to the parent task.';",
        "COMMENT ON COLUMN task_participants.participant_type IS 'Type of participant (usually LOAN).';",
        "COMMENT ON COLUMN task_participants.participant_id IS 'ID of the participant (e.g., Loan ID).';",
        "COMMENT ON COLUMN task_participants.payment_amount IS 'Amount collected during this task detail.';",

        # Agents
        "COMMENT ON TABLE agents IS 'Configuration for AI Agents in the system.';",
        "COMMENT ON COLUMN agents.role IS 'Role of the agent (COLLECTION, SALES, etc.).';",
        "COMMENT ON COLUMN agents.capabilities IS 'List of skills or tools the agent can use.';",

        # n8n Chat Histories
        "COMMENT ON TABLE n8n_chat_histories IS 'Storage for n8n AI chat memory/context.';",
        "COMMENT ON COLUMN n8n_chat_histories.session_id IS 'Session ID to track conversation threads.';",
        "COMMENT ON COLUMN n8n_chat_histories.message IS 'JSON object containing the chat message and metadata.';"
    ]

    for c in comments:
        try:
            cur.execute(c)
        except Exception as e:
            print(f"Warning: {e}")

    print("3. Creating get_list_of_tables_and_columns View...")
    # The complex query provided by user
    view_query = """
    CREATE OR REPLACE VIEW get_list_of_tables_and_columns AS
    WITH rels AS (SELECT c.oid,
                         n.nspname AS schema_name,
                         c.relname AS table_name,
                         c.relkind
                  FROM pg_class c
                           JOIN pg_namespace n ON n.oid = c.relnamespace
                  WHERE (c.relkind = ANY (ARRAY ['r'::"char", 'v'::"char", 'm'::"char"]))
                    AND (n.nspname <> ALL (ARRAY ['pg_catalog'::name, 'information_schema'::name, 'pg_toast'::name]))
                    AND n.nspname !~~ 'pg_temp%'::text
                    AND n.nspname !~~ 'pg_toast_temp%'::text),
         cols AS (SELECT r.schema_name,
                         r.table_name,
                         a.attnum,
                         a.attname                            AS column_name,
                         format_type(a.atttypid, a.atttypmod) AS data_type,
                         dc.description                       AS column_comment
                  FROM rels r
                           JOIN pg_attribute a ON a.attrelid = r.oid
                           LEFT JOIN pg_description dc ON dc.objoid = r.oid AND dc.objsubid = a.attnum
                  WHERE a.attnum > 0
                    AND NOT a.attisdropped),
         fk AS (SELECT n.nspname  AS schema_name,
                       c.relname  AS table_name,
                       a.attname  AS column_name,
                       nr.nspname AS ref_schema,
                       cr.relname AS ref_table,
                       ar.attname AS ref_column
                FROM pg_constraint con
                         JOIN pg_class c ON c.oid = con.conrelid
                         JOIN pg_namespace n ON n.oid = c.relnamespace
                         JOIN pg_class cr ON cr.oid = con.confrelid
                         JOIN pg_namespace nr ON nr.oid = cr.relnamespace
                         JOIN LATERAL unnest(con.conkey) WITH ORDINALITY ck(attnum, ord) ON true
                         JOIN LATERAL unnest(con.confkey) WITH ORDINALITY fk(attnum, ord) ON fk.ord = ck.ord
                         JOIN pg_attribute a ON a.attrelid = con.conrelid AND a.attnum = ck.attnum
                         JOIN pg_attribute ar ON ar.attrelid = con.confrelid AND ar.attnum = fk.attnum
                WHERE con.contype = 'f'::"char"),
         tcomm AS (SELECT n.nspname      AS schema_name,
                          c.relname      AS table_name,
                          dt.description AS table_comment
                   FROM pg_class c
                            JOIN pg_namespace n ON n.oid = c.relnamespace
                            LEFT JOIN pg_description dt ON dt.objoid = c.oid AND dt.objsubid = 0),
         fmt AS (SELECT c.schema_name,
                        c.table_name,
                        string_agg(((c.column_name::text || ' '::text) || c.data_type) || COALESCE(
                                (SELECT (((((' [FK→'::text || f_1.ref_schema::text) || '.'::text) || f_1.ref_table::text) ||
                                          '('::text) || f_1.ref_column::text) || ')]'::text
                                 FROM fk f_1
                                 WHERE f_1.schema_name = c.schema_name
                                   AND f_1.table_name = c.table_name
                                   AND f_1.column_name = c.column_name
                                 LIMIT 1), ''::text), ', '::text ORDER BY c.attnum)                        AS columns_with_types_and_columns,
                        jsonb_agg(jsonb_build_object('column_name', c.column_name, 'data_type', c.data_type, 'comment',
                                                     c.column_comment, 'fk', (SELECT CASE
                                                                                         WHEN f_1.ref_table IS NULL
                                                                                             THEN NULL::text
                                                                                         ELSE
                                                                                             ((((f_1.ref_schema::text || '.'::text) || f_1.ref_table::text) ||
                                                                                               '('::text) ||
                                                                                              f_1.ref_column::text) || ')'::text
                                                                                         END AS "case"
                                                                              FROM fk f_1
                                                                              WHERE f_1.schema_name = c.schema_name
                                                                                AND f_1.table_name = c.table_name
                                                                                AND f_1.column_name = c.column_name
                                                                              LIMIT 1))
                                  ORDER BY c.attnum)                                                       AS columns_detailed_json
                 FROM cols c
                 GROUP BY c.schema_name, c.table_name)
    SELECT DISTINCT ON (f.table_name) f.table_name,
                                      f.columns_with_types_and_columns,
                                      tc.table_comment,
                                      f.columns_detailed_json
    FROM fmt f
             LEFT JOIN tcomm tc ON tc.schema_name = f.schema_name AND tc.table_name = f.table_name
    ORDER BY f.table_name,
             (
                 CASE f.schema_name
                     WHEN 'erp'::name THEN 1
                     WHEN 'public'::name THEN 2
                     ELSE 9
                     END);
    """
    cur.execute(view_query)
    
    print("Done! Schema applied successfully.")
    conn.close()

if __name__ == "__main__":
    apply_schema()
