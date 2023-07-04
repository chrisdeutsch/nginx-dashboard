FROM python:3.11-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY nginx_dashboard nginx_dashboard
COPY app.py app.py

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "app:server"]
