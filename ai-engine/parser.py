import psycopg2
import re
from transformers import pipeline

DB_PARAMS = {
    "host": "localhost",
    "database": "ledgai",
    "user": "postgres",
    "password": "akshat125", 
    "port": "5432"
}

raw_statement_data = [
    {"date": "2026-05-20", "amount": 450.00, "info": "UPI/382910/MCDONALDS_PUNE/ICICI/Food"},
    {"date": "2026-05-21", "amount": 1200.00, "info": "UPI/938492/RAHUL_STORES_BANGALORE/HDFC"},
    {"date": "2026-05-22", "amount": 150.00, "info": "AMZN_MKTP_US_28394_SEATTLE"},
    {"date": "2026-05-23", "amount": 2500.00, "info": "ZOMATO_PUNE_ORDER_8293"},
]

print("Initializing local NLP classification pipeline...")
# Load a lightweight, high-performance zero-shot classification model
classifier = pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-1")

# Pre-defined transaction categories
CANDIDATE_CATEGORIES = ["Food & Dining", "Shopping & E-commerce", "Groceries", "Utilities & Bills"]

def clean_merchant_string(raw_string):
    """Tier 1: Fast Regex Basic Filter"""
    text = raw_string.upper()
    text = re.sub(r'UPI/\d+/', '', text)
    text = re.sub(r'_(PUNE|BANGALORE|SEATTLE|MUMBAI|DELHI)', '', text)
    text = re.sub(r'_(ORDER|MKTP|US|ICICI|HDFC)\S*', '', text)
    return text.replace('_', ' ').strip()

def process_and_seed_ledger():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        
        # Ensure our target categories exist in the lookup table and fetch IDs
        category_map = {}
        for cat in CANDIDATE_CATEGORIES:
            cur.execute("INSERT INTO categories (category_name) VALUES (%s) ON CONFLICT (category_name) DO UPDATE SET category_name=EXCLUDED.category_name RETURNING category_id;", (cat,))
            category_map[cat] = cur.fetchone()[0]

        # Fetch or seed our master test user
        cur.execute("INSERT INTO users (name, email) VALUES ('Akshat Test', 'testuser@ledgai.com') ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name RETURNING user_id;")
        user_id = cur.fetchone()[0]
        
        print("\n--- Running AI Ingestion Processing ---")
        for row in raw_statement_data:
            base_cleaned = clean_merchant_string(row["info"])
            
            # Tier 2 NLP Classification: Predict category and compute accuracy confidence scores
            res = classifier(base_cleaned, candidate_labels=CANDIDATE_CATEGORIES)
            best_category = res['labels'][0]
            confidence_score = res['scores'][0] * 100 # Convert to percentage
            
            # Deep clean the final corporate name by removing residual trailing bank flags
            final_merchant_name = re.sub(r'/(ICICI|HDFC|FOOD|SBI|AXIS)$', '', base_cleaned).strip()
            
            target_cat_id = category_map[best_category]
            
            print(f"Raw: {row['info'][:25]}... -> AI Merchant: {final_merchant_name} | Label: {best_category} ({confidence_score:.1f}%)")
            
            # Save the enriched data back into PostgreSQL
            cur.execute("""
                INSERT INTO transactions (user_id, category_id, amount, raw_merchant_string, cleaned_merchant_name, confidence_score, transaction_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (user_id, target_cat_id, row["amount"], row["info"], final_merchant_name, confidence_score, row["date"]))
            
        conn.commit()
        print("\n[SUCCESS] AI processing complete. Rows successfully populated with labels!")
        
        cur.close()
        conn.close()
        
    except Exception as error:
        print(f"\n[AI PIPELINE ERROR] Failed processing run: {error}")

if __name__ == "__main__":
    process_and_seed_ledger()