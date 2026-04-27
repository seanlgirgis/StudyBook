CREATE TABLE IF NOT EXISTS pipeline_runs (
    id SERIAL PRIMARY KEY,
    run_name TEXT NOT NULL,
    container_name TEXT NOT NULL DEFAULT 'unknown',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

INSERT INTO pipeline_runs (run_name, container_name)
VALUES ('compose_stack_initialized', 'init_db')
ON CONFLICT DO NOTHING;
