#!/bin/bash

set -e  # stop if any command fails

echo "Pulling latest code..."
git pull origin main

echo "Activating virtualenv..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Restarting gunicorn..."
sudo systemctl restart gunicorn

echo "Deployment finished successfully!"#!/bin/bash

echo "Pulling latest code..."
git pull origin main

echo "Activating virtualenv..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Restarting gunicorn..."
sudo systemctl restart gunicorn

echo "Deployment finished successfully!"
