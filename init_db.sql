
-- Automotas AI Test Database Initialization
-- ==========================================

-- Create extensions for testing
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create test schemas
CREATE SCHEMA IF NOT EXISTS test_data;
CREATE SCHEMA IF NOT EXISTS test_results;
CREATE SCHEMA IF NOT EXISTS test_history;

-- Test data tables for seeding
CREATE TABLE IF NOT EXISTS test_data.sample_agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100) NOT NULL,
    description TEXT,
    configuration JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS test_data.sample_workflows (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    steps JSONB NOT NULL,
    configuration JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS test_data.sample_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Test results tables
CREATE TABLE IF NOT EXISTS test_results.test_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    test_run_id VARCHAR(255) UNIQUE NOT NULL,
    environment VARCHAR(50) NOT NULL,
    total_tests INTEGER NOT NULL DEFAULT 0,
    passed INTEGER NOT NULL DEFAULT 0,
    failed INTEGER NOT NULL DEFAULT 0,
    skipped INTEGER NOT NULL DEFAULT 0,
    success_rate DECIMAL(5,2),
    duration DECIMAL(10,3),
    status VARCHAR(20) NOT NULL,
    started_at TIMESTAMP WITH TIME ZONE NOT NULL,
    completed_at TIMESTAMP WITH TIME ZONE,
    configuration JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS test_results.test_cases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    test_run_id UUID REFERENCES test_results.test_runs(id),
    test_suite VARCHAR(255) NOT NULL,
    test_name VARCHAR(255) NOT NULL,
    status VARCHAR(20) NOT NULL,
    duration DECIMAL(10,3),
    error_message TEXT,
    error_details JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS test_results.performance_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    test_run_id UUID REFERENCES test_results.test_runs(id),
    metric_name VARCHAR(255) NOT NULL,
    metric_value DECIMAL(15,6),
    metric_unit VARCHAR(50),
    endpoint VARCHAR(255),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Seed test data
INSERT INTO test_data.sample_agents (name, type, description, configuration) VALUES
('TestAgent1', 'code_architect', 'Test agent for code architecture', '{"priority": "normal", "skills": ["code_analysis", "architecture_design"]}'),
('TestAgent2', 'security_expert', 'Test agent for security analysis', '{"priority": "high", "skills": ["vulnerability_scanning", "threat_modeling"]}'),
('TestAgent3', 'performance_optimizer', 'Test agent for performance optimization', '{"priority": "normal", "skills": ["performance_analysis", "optimization"]}');

INSERT INTO test_data.sample_workflows (name, type, steps, configuration) VALUES
('TestWorkflow1', 'sequential', '[{"name": "step1", "type": "analysis"}, {"name": "step2", "type": "validation"}]', '{"timeout": 300}'),
('TestWorkflow2', 'parallel', '[{"name": "step1", "type": "security_scan"}, {"name": "step2", "type": "performance_test"}]', '{"max_parallel": 2}');

INSERT INTO test_data.sample_documents (title, content, metadata) VALUES
('Test Document 1', 'This is a test document for context engineering validation. It contains sample text for embedding generation and similarity testing.', '{"type": "test", "source": "framework"}'),
('Test Document 2', 'Another test document focusing on multi-agent systems and collaboration patterns. This document tests document processing capabilities.', '{"type": "test", "source": "framework"}');

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_test_runs_environment ON test_results.test_runs(environment);
CREATE INDEX IF NOT EXISTS idx_test_runs_status ON test_results.test_runs(status);
CREATE INDEX IF NOT EXISTS idx_test_runs_created_at ON test_results.test_runs(created_at);
CREATE INDEX IF NOT EXISTS idx_test_cases_test_run_id ON test_results.test_cases(test_run_id);
CREATE INDEX IF NOT EXISTS idx_test_cases_status ON test_results.test_cases(status);
CREATE INDEX IF NOT EXISTS idx_performance_metrics_test_run_id ON test_results.performance_metrics(test_run_id);

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA test_data TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA test_results TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA test_history TO postgres;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA test_data TO postgres;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA test_results TO postgres;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA test_history TO postgres;

-- Create views for common queries
CREATE OR replace VIEW test_results.latest_test_runs AS
SELECT 
    test_run_id,
    environment,
    total_tests,
    passed,
    failed,
    success_rate,
    duration,
    status,
    completed_at
FROM test_results.test_runs 
ORDER BY completed_at DESC 
LIMIT 10;

CREATE OR REPLACE VIEW test_results.test_suite_summary AS
SELECT 
    tr.environment,
    tc.test_suite,
    COUNT(*) as total_cases,
    COUNT(*) FILTER (WHERE tc.status = 'passed') as passed_cases,
    COUNT(*) FILTER (WHERE tc.status = 'failed') as failed_cases,
    ROUND(AVG(tc.duration), 3) as avg_duration
FROM test_results.test_runs tr
JOIN test_results.test_cases tc ON tr.id = tc.test_run_id
WHERE tr.completed_at >= NOW() - INTERVAL '30 days'
GROUP BY tr.environment, tc.test_suite
ORDER BY tr.environment, tc.test_suite;

-- Performance tracking view
CREATE OR REPLACE VIEW test_results.performance_trends AS
SELECT 
    DATE_TRUNC('day', pm.timestamp) as date,
    pm.metric_name,
    pm.endpoint,
    AVG(pm.metric_value) as avg_value,
    MIN(pm.metric_value) as min_value,
    MAX(pm.metric_value) as max_value
FROM test_results.performance_metrics pm
WHERE pm.timestamp >= NOW() - INTERVAL '30 days'
GROUP BY DATE_TRUNC('day', pm.timestamp), pm.metric_name, pm.endpoint
ORDER BY date DESC, metric_name;

COMMIT;
