
## Запуск проекта

### Требования

Установить [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Инструкция

1. Скачать репозиторий:
```bash
   git clone https://github.com/твой_логин/bookstore.git
   cd bookstore
```

2. Создать файл `.env` в корне проекта:
```bash
SECRET_KEY=django-insecure-bookstore-secret-key-change-in-production
DEBUG=False
DB_NAME=bookstore
DB_USER=bookuser
DB_PASSWORD=240472
DB_HOST=db
DB_PORT=5432
REDIS_URL=redis://redis:6379/0
```

3. Запустить контейнеры:
```bash
   docker compose up -d
```

4. Открыть браузер: [http://localhost](http://localhost)

### Данные для входа в админку

- Адрес: [http://localhost/admin](http://localhost/admin)
- Логин: `Администратор`
- Пароль: `Абакан19`

### Остановка проекта

```bash
docker compose down
```