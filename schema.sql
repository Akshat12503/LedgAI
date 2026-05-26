-- 1. Enable the pgvector extension for our AI RAG memory
CREATE EXTENSION IF NOT EXISTS pgvector;

-- 2. USERS TABLE
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. CATEGORIES TABLE (Food, Shopping, Rent, etc.)
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL UNIQUE,
    budget_limit NUMERIC(12, 2) DEFAULT 0.00
);

-- 4. TRANSACTIONS LEDGER TABLE (The core financial history)
CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    category_id INT REFERENCES categories(category_id) ON DELETE SET NULL,
    amount NUMERIC(12, 2) NOT NULL,
    raw_merchant_string VARCHAR(255) NOT NULL, -- The messy string from bank/UPI
    cleaned_merchant_name VARCHAR(100),         -- The name cleaned by AI
    confidence_score NUMERIC(5, 2),             -- How sure the AI was (e.g., 95.50)
    transaction_date TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. CHAT MEMORY TABLE (Vector store for RAG)
CREATE TABLE chat_memories (
    memory_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    conversation_id VARCHAR(100) NOT NULL,       -- Keeps track of the current session
    speaker VARCHAR(10) NOT NULL,                -- 'user' or 'copilot'
    text_content TEXT NOT NULL,                  -- The actual message text
    embedding vector(384),                       -- Vector array for 384-dimension local models
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);