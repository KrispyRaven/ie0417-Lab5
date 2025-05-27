FROM python:3.9-slim

# Instalar dependencias del sistema (usando netcat-openbsd)
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY datos.sh /app/datos.sh
RUN chmod +x /app/datos.sh
RUN mkdir -p /app/staticfiles

EXPOSE 8000

#CMD ["bash", "-c", "while ! nc -z db 5432; do sleep 2; echo 'Waiting for DB...'; done && python manage.py migrate && python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8000 myapp.wsgi"]python manage.py makemigrations
ENTRYPOINT ["/app/datos.sh"]