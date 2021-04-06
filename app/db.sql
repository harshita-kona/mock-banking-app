GRANT CONNECT ON DATABASE banking TO admin;
GRANT USAGE ON SCHEMA public TO admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin;

CREATE TABLE users (user_no SERIAL PRIMARY KEY, email_id UNIQUE VARCHAR(255) UNIQUE NOT NULL, customer_id VARCHAR(255) UNIQUE NOT NULL, first_name VARCHAR(255) NOT NULL, middle_name VARCHAR(255) NOT NULL, last_name VARCHAR(255) NOT NULL, date_of_birth DATE NOT NULL, occupation VARCHAR(255) NOT NULL,mobile_no VARCHAR(10) NOT NULL, created_date TIMESTAMP, password text NOT NULL);

CREATE TABLE branches (branch_no SERIAL PRIMARY KEY, branch_id VARCHAR(255) UNIQUE NOT NULL, branch_name VARCHAR(255) NOT NULL, branch_city VARCHAR(255) NOT NULL, created_date TIMESTAMP);

CREATE TABLE accounts (account_id SERIAL PRIMARY KEY, account_no VARCHAR(255) UNIQUE NOT NULL, customer_id VARCHAR(255) NOT NULL, branch_id VARCHAR(255) NOT NULL, opening_balance INTEGER NOT NULL, current_balance INTEGER NOT NULL, account_type VARCHAR(255) NOT NULL, account_status VARCHAR(255) NOT NULL, account_created_date TIMESTAMP, CONSTRAINT account_custid_fk FOREIGN KEY(customer_id) REFERENCES users(customer_id), CONSTRAINT account_bid_fk FOREIGN KEY(branch_id) REFERENCES branches(branch_id));

CREATE TABLE transactions (transaction_id SERIAL PRIMARY KEY, transaction_no VARCHAR(255) UNIQUE NOT NULL, account_no VARCHAR(255) NOT NULL, medium_of_transaction VARCHAR(255) NOT NULL, transaction_type VARCHAR(255) NOT NULL, amount INTEGER NOT NULL, balance INTEGER NOT NULL, transaction_date TIMESTAMP, CONSTRAINT transactions_acnumber_fk FOREIGN KEY(account_no) REFERENCES accounts(account_no));