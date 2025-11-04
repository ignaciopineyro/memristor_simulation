#!/bin/bash

set -e

echo "Initializing Memristor Simulation Application"

export DOCKER_ENV=1

sleep 2

echo "Veryfying NGSpice installation..."
ngspice -v || echo "NGSpice may not be available"

echo "Running Django migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Creating superuser if not exists..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists.')
"

echo "Veryfiying and creating necessary directories..."
mkdir -p /app/memristorsimulation_app/simulation_results/pershin_simulations
mkdir -p /app/memristorsimulation_app/simulation_results/vourkas_simulations
mkdir -p /app/staticfiles
mkdir -p /app/logs

echo "Configuration complete."

echo "Starting Django server on port 8000..."
echo "The application will be available at: http://localhost:8000"
echo "Admin panel at: http://localhost:8000/admin (admin/admin123)"

exec python manage.py runserver 0.0.0.0:8000