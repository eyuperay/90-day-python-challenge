-- PostgreSQL initialization script
CREATE TABLE IF NOT EXISTS visit (
    id SERIAL PRIMARY KEY,
    ip VARCHAR(50),
    user_agent VARCHAR(200),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO visit (ip, user_agent, timestamp) VALUES 
    ('192.168.1.1', 'Sample User Agent 1', NOW()),
    ('192.168.1.2', 'Sample User Agent 2', NOW()),
    ('192.168.1.3', 'Sample User Agent 3', NOW())
ON CONFLICT DO NOTHING;

-- Create index
CREATE INDEX IF NOT EXISTS idx_visit_timestamp ON visit(timestamp);

-- Grant privileges
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO postgres;
