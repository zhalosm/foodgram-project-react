# Продуктовый помощник - Foodgram

На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, 
добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, 
необходимых для приготовления одного или нескольких выбранных блюд.

Сайт доступен по адресу http://158.160.0.75/

# Workflow

- проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8) и запуск pytest
- сборка и доставка докер-образа для контейнера web на Docker Hub
- автоматический деплой проекта на боевой сервер
- отправка уведомления в Telegram о том, что процесс деплоя успешно завершился

### ![example workflow](https://github.com/zhalosm/foodgram-project-react/actions/workflows/main.yml/badge.svg)

# Стэк технологий

- Python
- Django Rest Framework
- Postgres
- PostgreSQL
- Docker
- nginx
- Github Actions

# Запуск проекта в контейнере

Клонировать репозиторий:

```
git@github.com:zhalosm/foodgram-project-react.git
```

Перейти в папку с файлом docker-compose.yaml:

```
cd infra
```

Собираем контйенеры и запускаем их:

```
docker-compose up -d --build
```

Выполняем миграцию:

```
docker-compose exec web python manage.py migrate
```

Создаем суперпользователя:

```
docker-compose exec web python manage.py createsuperuser
```

Собираем статику:

```
docker-compose exec web python manage.py collectstatic --no-input
```

Cоздание дамп (резервной копии) базы:

```
docker-compose exec web python manage.py dumpdata > fixtures.json
```

Остновка и удаление контйенров.

```
docker-compose down -v
```

# Шалблон наполнения env-файла:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
# Запуск проекта на удаленном сервере

Остановите службу nginx

```
sudo systemctl stop nginx
```

Установите Docker 

```
sudo apt install docker.io
```

Установите Docker-compose https://docs.docker.com/compose/install/

Скопируйте файлы docker-compose.yaml и nginx/default.conf из вашего проекта на сервер в 
home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/default.conf соответственно.

```
scp docker-compose.yaml <username>@<host>/home/<username>/docker-compose.yaml
sudo mkdir nginx
scp default.conf <username>@<host>/home/<username>/nginx/default.conf
```

Добавьте в Secrets GitHub Actions данные:

```
DOCKER_USERNAME = имя пользователя в DockerHub
DOCKER_PASSWORD = пароль пользователя в DockerHub
HOST = ip-адрес сервера
USER = пользователь
SSH_KEY = приватный ключ с компьютера, имеющего доступ к серверу
PASSPHRASE = пароль для ssh-ключа
DB_ENGINE = django.db.backends.postgresql
DB_HOST = db
DB_PORT = 5432
DB_NAME = postgres 
POSTGRES_USER = postgres 
POSTGRES_PASSWORD = postgres
TELEGRAM_TO = id своего телеграм-аккаунта
TELEGRAM_TOKEN = токен бота
```

# После успешного деплоя

Выполняем миграцию:

```
sudo docker-compose exec web python manage.py migrate
```

Создаем суперпользователя:

```
sudo docker-compose exec web python manage.py createsuperuser
```

Собираем статику:

```
sudo docker-compose exec web python manage.py collectstatic --no-input
```

### Автор проекта:

### Петров Константин