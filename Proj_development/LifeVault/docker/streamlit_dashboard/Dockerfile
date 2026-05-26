FROM python:3.11-slim

WORKDIR /workspace

RUN pip install --no-cache-dir streamlit

EXPOSE 8501

CMD ["streamlit", "run", "app/streamlit/lifevault_help_console.py", "--server.address=0.0.0.0", "--server.port=8501"]
