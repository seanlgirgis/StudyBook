# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install requirements
COPY src/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code package into /app/src
COPY src/ ./src

# Copy data and outputs

COPY data/ ./data

COPY outputs/ ./outputs

# Copy test files
COPY ../tests/ ./tests

# ---- NEW: Copy config folder ----
COPY config/ ./config

EXPOSE 8000

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
