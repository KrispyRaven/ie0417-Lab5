# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requisitos
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Recolectar archivos estáticos (si es necesario)
RUN python manage.py collectstatic --noinput

# Aplicar migraciones
RUN python manage.py migrate

# Puerto que expone la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]