#!/usr/bin/env bash
# Exit on error
set -o errexit

# 1. Build Frontend
cd frontend
npm install
npm run build
cd ..

# 2. Build Backend
cd backend
pip install -r requirements.txt

# 3. Copy React build to Django static files
cp -r ../frontend/dist/* .
python manage.py collectstatic --no-input
python manage.py migrate
