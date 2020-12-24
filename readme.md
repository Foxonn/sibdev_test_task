## Инструкция по запуску сервиса

1. `git clone https://github.com/Foxonn/sibdev_test_task`
2. `docker-compose up --build`
3. В контейнере django_app, запустить миграцию `python manage.py migrate`

### API

- post
    - `/api/v1/upload/` - загрузка файла.
        - аргументы:
            - `deals` - принимает файл типа csv.
- get
    - `/api/v1/five_best_clients/` - получение списка из пяти
      клиентов которые потратили наибольшее количество средств и которые купили
      мимнимум два таких же камня, что и другие из этого списка.