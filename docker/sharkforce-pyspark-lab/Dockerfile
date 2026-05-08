FROM python:3.12-bookworm

LABEL name="sharkforce-pyspark-lab"
LABEL purpose="Local PySpark, notebooks, data quality, entity resolution, interview prep"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYSPARK_PYTHON=python \
    PYSPARK_DRIVER_PYTHON=python \
    PYTHONPATH=/workspace/project/src \
    JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64 \
    SPARK_LOCAL_IP=127.0.0.1 \
    SPARK_DRIVER_HOST=127.0.0.1 \
    PYARROW_IGNORE_TIMEZONE=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    curl \
    wget \
    procps \
    tini \
    openjdk-17-jre-headless \
    build-essential \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY requirements.txt /workspace/requirements.txt

RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r /workspace/requirements.txt

RUN mkdir -p \
    /workspace/project \
    /workspace/notebooks \
    /workspace/data \
    /workspace/data/spark-warehouse \
    /workspace/data/delta \
    /workspace/src \
    /workspace/tests \
    /workspace/outputs

EXPOSE 8888 4040

ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--ServerApp.token=", "--ServerApp.password=", "--ServerApp.allow_origin=*", "--ServerApp.root_dir=/workspace/project"]