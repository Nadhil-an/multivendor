#!/bin/sh

# 1. Exit immediately if a command exits with a non-zero status.
set -e

# 2. Perform database migrations
# This ensures your tables are created in the PostGIS database.
echo "Applying database migrations..."
python manage.py migrate --noinput

# 3. Collect static files
# This gathers all your CSS, JS, and images into one place for the web server.
echo "Collecting static files..."
python manage.py collectstatic --noinput

# 4. Execute the command that was passed to Docker (this keeps the container running)
exec "$@"
