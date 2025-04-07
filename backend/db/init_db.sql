-- Initialize database schema

-- Create schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS copilot;

-- Sessions table
CREATE TABLE IF NOT EXISTS copilot.sessions (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER,
    therapeutic_area VARCHAR(255),
    trial_phase VARCHAR(50),
    trial_condition VARCHAR(255),
    trial_intent VARCHAR(255),
    file_summary TEXT,
    ai_insights JSONB,
    state JSONB,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    company_name VARCHAR(255),
    company_website VARCHAR(255),
    nct_id VARCHAR(50)
);

-- Uploads table
CREATE TABLE IF NOT EXISTS copilot.uploads (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES copilot.sessions(id),
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(512) NOT NULL,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- File insights table
CREATE TABLE IF NOT EXISTS copilot.file_insights (
    id SERIAL PRIMARY KEY,
    upload_id INTEGER REFERENCES copilot.uploads(id),
    insights JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Intake forms table
CREATE TABLE IF NOT EXISTS copilot.intake_forms (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES copilot.sessions(id),
    form_data JSONB NOT NULL,
    processed_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
