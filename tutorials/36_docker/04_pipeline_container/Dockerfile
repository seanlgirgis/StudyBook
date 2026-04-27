FROM python:3.11.9-slim-bookworm

ARG APP_VERSION=1.0.0

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_VERSION=${APP_VERSION}

WORKDIR /app

COPY requirements.txt .
RUN if [ -s requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

COPY app/ ./app/

RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --shell /usr/sbin/nologin --create-home appuser && \
    mkdir -p /data/input /data/output && \
    chown -R appuser:appgroup /app /data

USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import pathlib, sys; sys.exit(0 if pathlib.Path('/app/app/graceful_pipeline.py').exists() else 1)"

ENTRYPOINT ["python"]
CMD ["app/graceful_pipeline.py"]
