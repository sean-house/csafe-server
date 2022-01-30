#!/bin/bash
set -e

# echo "Starting SSH ..."
service ssh start

#echo "Starting CSAFE server"
#echo $PWD
#echo $AZURE_USERNAME
#echo $CSAFE_KEY
#echo $CSAFE_INTENT
#python manage.py runserver 0.0.0.0:8000

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn csafe.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3
