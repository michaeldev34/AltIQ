#!/bin/bash

# Install Node dependencies and build Tailwind CSS
npm install
npm run build:css

# Collect static files
python3.11 -m pip install -r requirements.txt
python3.11 manage.py collectstatic --noinput

