#!/bin/bash

# Install Node dependencies and build Tailwind CSS
npm install
npm run build:css

# Collect static files
pip install -r requirements.txt
python manage.py collectstatic --noinput

