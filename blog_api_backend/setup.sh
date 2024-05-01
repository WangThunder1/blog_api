#!/bin/bash
# Name of the Docker container running Django
CONTAINER_NAME="blog_api_backend"
# Django project directory in the container
DJANGO_DIR="/code"
# Remove existing migrations if they exist
docker exec $CONTAINER_NAME find $DJANGO_DIR -path "*/migrations/*.py" -not -name "__init__.py" -delete
docker exec $CONTAINER_NAME find $DJANGO_DIR -path "*/migrations/*.pyc"  -delete
# Do migrations stuff
docker exec $CONTAINER_NAME python manage.py makemigrations
docker exec $CONTAINER_NAME python manage.py migrate
# Collect static files
docker exec $CONTAINER_NAME python manage.py collectstatic --noinput
# Create superuser (Modify username and email as needed)
docker exec -it $CONTAINER_NAME python manage.py createsuperuser --username admin --email admin@example.com --noinput
echo "from django.contrib.auth import get_user_model; User = get_user_model(); user = User.objects.get(username='admin'); user.set_password('admin'); user.save()" | docker exec -i $CONTAINER_NAME python manage.py shell