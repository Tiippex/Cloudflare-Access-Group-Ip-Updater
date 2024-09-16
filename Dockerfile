FROM python:3.9-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY updateCloudflareIp.py .

RUN chmod +x updateCloudflareIp.py

CMD ["./updateCloudflareIp.py"]