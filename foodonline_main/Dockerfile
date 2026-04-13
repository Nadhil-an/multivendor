# 1. Use the official Python 'slim' image for a lightweight foundation
FROM python:3.11-slim

# 2. Environment variables to make Python output logs correctly and stay clean
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# 3. Set the working directory inside the container
WORKDIR /app

# 4. CRITICAL: Install system libraries (GDAL, GEOS, PROJ)
# These are required by Django for your location and map features.
RUN apt-get update \
    && apt-get install -y \
    libgdal-dev \
    libproj-dev \
    libgeos-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 5. Copy requirements first to help Docker cache them (making future builds faster)
COPY requirements.txt /app/

# 6. Install your Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 7. Copy the rest of your application code
COPY . /app/

# 8. Expose the port where the app will run (8000 is default for Django)
EXPOSE 8000

# 9. Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# Copy the entrypoint script and make it executable
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Tell Docker to use this script every time the container starts
ENTRYPOINT ["docker-entrypoint.sh"]
