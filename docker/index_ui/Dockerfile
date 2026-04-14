FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_HEADLESS=true

WORKDIR /app

COPY docker/index_ui/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY coding_challenges/scripts/index_ui_streamlit.py /app/coding_challenges/scripts/index_ui_streamlit.py
COPY coding_challenges/index.csv /app/coding_challenges/index.csv

EXPOSE 8501

CMD ["streamlit", "run", "coding_challenges/scripts/index_ui_streamlit.py", "--server.address", "0.0.0.0", "--server.port", "8501", "--browser.gatherUsageStats", "false"]
