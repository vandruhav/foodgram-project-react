# Дипломная работа Foodgram

[![Foodgram](https://github.com/vandruhav/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?branch=master)](http://vandruhav.sytes.net/recipes/)

На сайте создан суперпользователь для проверки проекта:
- email: super@super.ru
- password: super

## Стек технологий:
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
язык программирования Python 3.10.6.

[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
фреймворк Django 2.2.28 и DRF 3.12.4.

[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
контейнеризация Docker 20.10.21 и Docker-Compose 1.29.2.

[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
оптимизация и автоматизация DevOps и CI.

[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)
облачный сервер Yandex Cloud.

[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
WSGI-сервер Gunicorn 20.0.4.

[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
веб-сервер Nginx 1.19.3.

[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
СУБД PostgreSQL 13.0.

## Описание проекта
Foodgram - продуктовый помощник с базой кулинарных рецептов. Позволяет
публиковать рецепты, сохранять избранные, а также формировать список покупок
для выбранных рецептов. Можно подписываться на любимых авторов.

Проект состоит из сервисов, которые запакованы в отдельные контейнеры:
Django-приложение с сервером Gunicorn, база данных Postgres и веб-сервер Nginx.
Образы проекта (frontend и backend) находятся на DockerHub, скачать их можно
командами:
```
sudo docker pull vandruhav/foodgram_frontend:v1
sudo docker pull vandruhav/foodgram_backend:v1
```

## Разворачивание проекта на удаленном сервере
1. На удалённом сервере установите Docker и надстройку Docker-Compose:
```
sudo apt install curl
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo apt install docker-compose -y
```
2. На локальный компьютер склонируйте репозиторий foodgram-project-react с
GitHub.com:
```
git clone git@github.com:vandruhav/foodgram-project-react.git
```
3.На локальном компьютере отредактируйте файл infra/nginx.conf и в строке
server_name впишите <IP_вашего_сервера>. Находясь в корневой папке проекта,
скопируйте с локального компьютера на удалённый сервер директории infra и docs:
```
scp -r infra <ваш_username_на_сервере>@<IP_вашего_сервера>:~/
scp -r docs <ваш_username_на_сервере>@<IP_вашего_сервера>:~/
```
4. В домашней директории на удалённом сервере создайте файл .env:
```
touch .env
```
Содержимое файла .env:
- SECRET_KEY - ключ к защите подписанных данных
- DEBUG - ключ отладки приложения
- ALLOWED_HOSTS - список хостов/доменов, для которых может работать проект,
<IP_вашего_сервера>
- DB_ENGINE - используемый движок для доступа к БД
- DB_NAME - имя БД
- POSTGRES_USER - логин для подключения к БД
- POSTGRES_PASSWORD - пароль для подключения к БД
- DB_HOST - название сервиса (контейнера)
- DB_PORT - порт для подключения к БД
5. Перейдите в директорию infra на удалённом сервере:
```
cd ~/infra
```
6. Соберите контейнеры и запустите их на удалённом сервере:
```
sudo docker-compose up -d
```
7. Создайте скрипты миграций в контейнере web на удалённом сервере:
```
sudo docker-compose exec web python manage.py makemigrations
```
8. Выполните миграции в контейнере web на удалённом сервере:
```
sudo docker-compose exec web python manage.py migrate
```
9. Создайте суперпользователя в контейнере web на удалённом сервере:
```
sudo docker-compose exec web python manage.py createsuperuser
```
10. Соберите статику в контейнере web на удалённом сервере:
```
sudo docker-compose exec web python manage.py collectstatic --noinput
```
11. Для заполнения БД данными, предоставленными с проектом, используйте
команду (опционально):
```
sudo docker-compose exec web python manage.py fill_db
```
12. Проект доступен, все функции и эндпойнты описаны в документации:
```
http://<IP_вашего_сервера>/api/docs/
```

## Работа с GitHub Actions
После каждого обновления репозитория в ветке master будет запускаться:
- Проверка кода на соответствие стандарту PEP8
- Сборка и сохранение образов frontend и backend на Docker Hub
- Разворачивание проекта на удаленном сервере
- В случае успеха отправка сообщения в Telegram

Для работы с GitHub Actions необходимо в репозитории в разделе
Secrets > Actions создать переменные окружения:
- SECRET_KEY - ключ к защите подписанных данных
- DEBUG - ключ отладки приложения
- ALLOWED_HOSTS - список хостов/доменов, для которых может работать проект,
<IP_вашего_сервера>
- DB_ENGINE - используемый движок для доступа к БД
- DB_NAME - имя БД
- POSTGRES_USER - логин для подключения к БД
- POSTGRES_PASSWORD - пароль для подключения к БД
- DB_HOST - название сервиса (контейнера)
- DB_PORT - порт для подключения к БД
- DOCKER_PASSWORD - пароль от Docker Hub
- DOCKER_USERNAME - логин Docker Hub
- HOST - публичный IP удалённого сервера
- USER - имя пользователя на удалённом сервере
- SSH_KEY - приватный ssh-ключ
- PASSPHRASE - пароль ssh-ключа (если ssh-ключ защищён паролем)
- TELEGRAM_TO - ID телеграм-аккаунта для посылки сообщения
- TELEGRAM_TOKEN - токен телеграм-бота, посылающего сообщение

# (с) Дипломная работа Воробьёва Андрея. 2022
