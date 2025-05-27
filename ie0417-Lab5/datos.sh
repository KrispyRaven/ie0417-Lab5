#!/bin/sh

# Esperar a PostgreSQL con script Python
echo "🔄 Esperando base de datos..."
python wait_for_db.py

# Migraciones
echo "📦 Ejecutando migraciones..."
python manage.py migrate --noinput

python manage.py loaddata items

# Ejecutar el servidor
echo "🚀 Iniciando servidor..."
exec gunicorn myproject.wsgi:application --bind 0.0.0.0:8000


