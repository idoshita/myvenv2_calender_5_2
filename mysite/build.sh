#!/usr/bin/env bash
# exit on error

set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-install
python manage.py migrate
python manage.py superuser
