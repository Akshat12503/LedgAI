import psycopg2
import re

DB_PARAMS = {
    "host": "localhost",
    "database": "ledgai",
    "user": "postgres",
    "password": "akshat125", 
    "port": "5432"
}

# Raw messy dataset from the bank statement dump
raw_statement_data = [
    {"date": "2026-05-20", "amount": 450.00, "info": "UPI/382910/MCDONALDS_PUNE/ICICI/Food"},
    {"date": "2026-05-21", "amount": 1200.00, "info": "UPI/938492/RAHUL_STORES_BANGALORE/HDFC"},
    {"date": "2026-05-22", "amount": 150.00, "info": "AMZN_MKTP_US_28394_SEATTLE"},
    {"date": "2026-05-23", "amount": 2500.00, "info": "ZOMATO_PUNE_ORDER_8293"},
]

def clean_merchant_string(raw_string):
    """Tier 1: Basic Regex Cleaning"""
    text = raw_string.upper()
    text = re.sub(r'UPI/\d+/', '', text)
    text = re.sub(r'_(PUNE|BANGALORE|SEATTLE|MUMBAI|DELHI)', '', text)
    text = re.sub(r'_(ORDER|MKTP|US|ICICI|HDFC)\S*', '', text)
    return text.replace('_', ' ').strip()

def insert_transaction_data():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        
        # 1. Seed a test profile to satisfy Foreign Key constraints
        print("Seeding test profile...")
        cur.execute("""
            INSERT INTO users (name, email) 
            VALUES ('Akshat Test', 'testuser@ledgai.com')
            ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name
            RETURNING user_id;
        """)
        user_id = cur.fetchone()[0]
        
        # 2. Loop through and run parameterized SQL inserts
        print("Processing and uploading transactions...")
        for row in raw_statement_data:
            cleaned_name = clean_merchant_string(row["info"])
            
            cur.execute("""
                INSERT INTO transactions (user_id, amount, raw_merchant_string, cleaned_merchant_name, transaction_date)
                VALUES (%s, %s, %s, %s, %s);
            """, (user_id, row["amount"], row["info"], cleaned_name, row["date"]))
            
        # 3. Commit the transactions to make changes permanent
        conn.commit()
        print("\n[SUCCESS] All cleaned entries successfully pushed to PostgreSQL ledger!")
        
        cur.close()
        conn.close()
        
    except Exception as error:
        print(f"\n[WRITE ERROR] Failed to push rows: {error}")

if __name__ == "__main__":
    insert_transaction_data()