FROM python:3.13.0a4-alpine

WORKDIR /app

COPY requirements.txt .
COPY main.py .
RUN pip install -r requirements.txt
CMD ["python3", "/app/main.py"]
