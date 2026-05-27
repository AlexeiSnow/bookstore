#!/bin/bash

echo "Ждём базу данных..."
while ! python manage.py showmigrations > /dev/null 2>&1; do
    sleep 1
done

echo "Применяем миграции..."
python manage.py migrate

echo "Загружаем начальные данные..."
python manage.py loaddata fixtures/initial_data.json

echo "Собираем статику..."
python manage.py collectstatic --noinput

echo "Запускаем сервер..."
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3