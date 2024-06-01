#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
cd frontend && npm install && npm run build
cd ..
python3 manage.py collectstatic --no-input
python3 manage.py migrate
