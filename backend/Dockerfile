FROM python:3.9-slim

WORKDIR /app/backend

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH=/app/backend

CMD ["python", "main.py"] 