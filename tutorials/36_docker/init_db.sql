CREATE TABLE IF NOT EXISTS pipeline_runs (
    id SERIAL PRIMARY KEY,
    run_name TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

INSERT INTO pipeline_runs (run_name)
VALUES ('compose_stack_initialized')
ON CONFLICT DO NOTHING;
