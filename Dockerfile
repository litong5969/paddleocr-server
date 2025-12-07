ARG PADDLE_IMAGE_TAG=3.2.2-gpu-cuda12.6-cudnn9.5
FROM paddlepaddle/paddle:${PADDLE_IMAGE_TAG}

WORKDIR /app

RUN apt update && apt install -y \
    python3-pip python3-dev \
    libglib2.0-0 libsm6 libxrender1 libxext6 libgl1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY server.py .
COPY web ./web

EXPOSE 5000

CMD ["python", "server.py"]
