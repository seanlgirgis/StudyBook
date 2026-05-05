FROM nvidia/cuda:13.0.1-runtime-ubuntu22.04

# Install Python 3, pip, git
RUN apt-get update -o Acquire::ForceIPv4=true && \
    apt-get install -y python3 python3-pip git && \
    rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy app
COPY app.py .

RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install Python packages including transformers and PyTorch
RUN pip install --no-cache-dir fastapi "uvicorn[standard]" transformers accelerate safetensors sentencepiece bitsandbytes

# Expose port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]