
# Informe Técnico - Laboratorio 5: Despliegue de una aplicación Django con Docker

## Diagrama de Arquitectura del Sistema

```mermaid
graph TD
    A[Navegador Web] -->|localhost:8080| B[Contenedor Django]
    B -->|Red Docker| C[Contenedor PostgreSQL]
    C --> D[(Volumen PostgreSQL)]
```

**Descripción:**  
- **Navegador Web:** Accede a la aplicación Django a través del puerto `8080`.  
- **Contenedor Django:** Ejecuta la aplicación web y se comunica con PostgreSQL a través de una red Docker personalizada.  
- **Contenedor PostgreSQL:** Almacena los datos de la aplicación. Utiliza un volumen para persistencia (`db_data`).  
- **Red Docker:** Conecta los contenedores Django y PostgreSQL.  

---

## Explicación de Archivos Clave

### 1. `Dockerfile` (Aplicación Django)
```dockerfile
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
```

**Funcionalidad:**  
- Crea una imagen basada en Python 3.9.  
- Instala dependencias desde `requirements.txt` (incluye Django, psycopg2-binary, y gunicorn).  
- Expone el puerto `8000` y ejecuta la aplicación con Gunicorn.  

---

### 2. `docker-compose.yml`
```yaml
version: '3.8'

services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/code
    working_dir: /code
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - PYTHONPATH=/code
      - DJANGO_SETTINGS_MODULE=myproject.settings

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

**Funcionalidad:**  
- **Servicio `web`:** Construye la imagen Django, mapea el puerto `8080` y usa variables de entorno.  
- **Servicio `db`:** Usa PostgreSQL 13, persiste datos en el volumen `db_data` y comparte la red `lab_network`.  

---


## Instrucciones para Ejecutar el Entorno

1. **Clonar el repositorio:**
   ```bash
   git clone <repositorio>
   cd <directorio>
   ```

2. **Crear y configurar `.env`:**
   ```bash
   cp .env.example .env
   # Editar .env con credenciales reales
   ```

3. **Construir y levantar los contenedores:**
   ```bash
   docker-compose up --build
   ```

4. **Aplicar migraciones (en otra terminal):**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Acceder a la aplicación:**  
   Abrir `http://localhost:8080` en el navegador.  

--

---

## Notas Finales
- **Reproducibilidad:** El entorno se inicia con un solo comando (`docker-compose up`).  
- **Buenas prácticas:** Uso de volúmenes, redes personalizadas y variables de entorno.  
- **Extensibilidad:** La estructura permite añadir más servicios (ej: Redis) fácilmente.  
``` 
