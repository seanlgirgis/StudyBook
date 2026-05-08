CREATE TABLE IF NOT EXISTS hello (
  id SERIAL PRIMARY KEY,
  note TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);
INSERT INTO hello (note) VALUES ('PostgreSQL container is ready!');
