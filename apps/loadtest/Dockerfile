FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/load_test.py .

CMD ["python", "load_test.py"] 