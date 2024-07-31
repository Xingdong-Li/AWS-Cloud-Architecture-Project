# Dockerfile
FROM python:3.8-slim

WORKDIR /
COPY ./app /app
COPY ./tests /tests
COPY ./requirements.txt /requirements.txt
COPY ./init.sh /init.sh
RUN chmod +x /init.sh
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r /requirements.txt

CMD ["sh", "-c", "while ! curl -s http://localstack:4566; do sleep 1; done && /init.sh && python /app/main.py"]
