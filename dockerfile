FROM python:3.10-slim

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /app

COPY app/main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]