#!/bin/sh

set -e

python manage.py wait_for_db
python manage.py collectstatic --noinput
chmod -R 777 /vol/cache/__pycache__/
#python manage.py migrate
