![](https://img.shields.io/badge/YaMDb-1.2.0-green) [![yamdb_workflow](https://github.com/tonik350/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/tonik350/yamdb_final/actions/workflows/yamdb_workflow.yml)
<br><br>
# YaMDb

## Запуск проекта:
### 1. В dev-режиме:
Клонировать репозиторий и перейти в него в командной строке:
```sh
git clone git@github.com:jood2302/infra_sp2.git
```
Установить и активировать виртуальное окружение:
```sh
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt
```sh
pip install -r requirements.txt
```
Выполнить миграции:
```sh
python manage.py migrate
``` 
Импортировать данные:
```sh
python manage.py loaddata fixtures.json
```
или из CSV-файла:
```sh
python manage.py import_from_csv <csv файл> <название модели>
```
В папке с файлом manage.py выполните команду:
```sh
python manage.py runserver
```

### 2. Запуск в контейнере Docker:
Создать файл `.env` внутри директории infra :

Заполнить переменные окружения в `.env`:
```sh
SECRET_KEY=<ваш секретный ключ Django>
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```

Прежде чем приступать к работе, убедиться что Docker установлен, для этого ввести команду:
   ```bash
   docker -v
   ```
В случае отсутствия, скачать [Docker Desktop](https://www.docker.com/products/docker-desktop) для Mac или Windows. [Docker Compose](https://docs.docker.com/compose) будет установлен автоматически.
В Linux проверить, что установлена последняя версия [Compose](https://docs.docker.com/compose/install/).

Также можно воспользоваться официальной [инструкцией](https://docs.docker.com/engine/install/).

Убедиться, что Docker установлен и готов к работе
```bash
docker --version
```
Запустите docker-compose
```bash
cd infra/
docker-compose up -d --build
```
Собрать статику и выполнить миграции внутри контейнера, создать суперпользователя:
```sh
docker-compose exec web python manage.py migrate --noinput
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```

## Деплой на удаленном сервере
Для запуска на удаленном сервере необходимо:
- перенести файлы `docker-compose.yaml` и папку `nginx` на сервер, выполнив команду:
```sh
scp -r ./infra/* <username>@<server_ip>:/home/<username>/
```
- на github, в настройках репозитория `Secrets` --> `Actions` создать и заполнить переменные окружения:
```sh
DOCKER_USERNAME # Имя пользователя на Docker Hub;
DOCKER_PASSWORD # Пароль от Docker Hub;
DB_ENGINE # Указать, что работаем с базой данных PostgresQl;
DB_NAME # Имя базы данных;
DB_HOST # Название контейнера базы данных; 
DB_PORT # Порт для подключения к базе данных;
POSTGRES_USER # Логин для подключения к базе данных;
POSTGRES_PASSWORD # Пароль для подключение к базе данных;
SECRET_KEY # Секретный ключ приложения;
USER # Имя пользователя на сервере;
HOST # Публичный IP-адрес сервера;
PASSPHRASE # Указать в том случае, если ssh-ключ защищен фразой-паролем;
SSH_KEY # Приватный ssh-ключ;
TELEGRAM_TO # ID телеграм-аккаунта;
TELEGRAM_TOKEN # Токен телеграм-бота.
```

### После каждого пуша (`git push`) в главную ветку `main`:
- будут автоматически запускаться тесты: проверка кода на соответствие стандарту `PEP8` (с помощью пакате `flake8`) и запуск `pytest` из репозитория `yamdb_final`;
- сборка и доставка докер-образа на `Docker Hub`;
- автоматический деплой на боевой сервер;
- отправка сообщения в `Telegram` при успешном завершении деплоя.

## Примеры запросов
### Ресурсы API YaMDb
- Ресурс `auth`: аутентификация.
- Ресурс `users`: пользователи.
- Ресурс `titles`: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- Ресурс `categories`: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
- Ресурс `genres`: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс `reviews`: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс `comments`: комментарии к отзывам. Комментарий привязан к определённому отзыву.

### Примеры запросов для неаутентифицированных пользователей:
* `api/v1/categories/` _(GET)_ - Получение списка всех категорий
* `api/v1/genres/` _(GET)_ - Получение списка всех жанров
* `api/v1/titles/` _(GET)_ - Получение списка всех произведений
* `api/v1/titles/{title_id}/reviews/` _(GET)_ - Получение списка всех отзывов
* `api/v1/titles/{title_id}/reviews/{review_id}/comments/` _(GET)_ - Получение списка всех комментариев к отзыву  

### Самостоятельная регистрация новых пользователей

Пользователь отправляет POST-запрос с параметрами email и username на эндпоинт: 
```
POST api/v1/auth/signup/
```
```
{
  "email": "string",
  "username": "string"
}
```

Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.
Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен):
```
POST api/v1/auth/token/
```
```
{
  "username": "string",
  "confirmation_code": "string"
}
```
В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом.
После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт /api/v1/users/me/ и заполнить поля в своём профайле (описание полей — в документации).

#### Примеры работы с API для авторизованных пользователей
Добавление категории:
```
Права доступа: Администратор.
POST api/v1/categories/
```
```
{
  "name": "string",
  "slug": "string"
}
```
Удаление категории:

```
Права доступа: Администратор.
DELETE api/v1/categories/{slug}/
```
Добавление жанра:

```
Права доступа: Администратор.
POST api/v1/genres/
```
```
 {
  "name": "string",
  "slug": "string"
}
```
Обновление публикации:

```
PUT api/v1/posts/{id}/
```
```
{
"text": "string",
"image": "string",
"group": 0
}
```
Добавление произведения:

```
Права доступа: Администратор. 
Нельзя добавлять произведения, которые еще не вышли (год выпуска не может быть больше текущего).
POST api/v1/titles/
```
```
 {
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
Обновление информации о произведении:

```
Права доступа: Администратор
PATCH api/v1/titles/{titles_id}/
```
```
 {
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
#### Работа с пользователями:
Получение списка всех пользователей:
```
Права доступа: Администратор
GET api/v1/users/ - Получение списка всех пользователей
```
Добавление пользователя:

```
Права доступа: Администратор
Поля email и username должны быть уникальными.
POST api/v1/users/ - Добавление пользователя
```
```
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
```
Получение пользователя по username:

```
Права доступа: Администратор
GET api/v1/users/{username}/ - Получение пользователя по username
```
Изменение данных пользователя по username:

```Права доступа: Администратор
PATCH api/v1/users/{username}/ - Изменение данных пользователя по username
```
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
Удаление пользователя по username:

```
Права доступа: Администратор
DELETE api/v1/users/{username}/ - Удаление пользователя по username
```
Подробная документация доступна по адресу `http://localhost/redoc/`
