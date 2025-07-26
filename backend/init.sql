-- Create the database if it doesn't exist
SELECT 'CREATE DATABASE ecommerce_chatbot'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'ecommerce_chatbot')\gexec

-- Connect to the database
\c ecommerce_chatbot;

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- You can add any additional database setup here
-- Tables will be created by SQLAlchemy
