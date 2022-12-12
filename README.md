# Дипломная работа Foodgram

[![Foodgram](https://github.com/vandruhav/foodgram-project-react/actions/workflows/foodgram.yml/badge.svg?branch=master)](http://vandruhav.sytes.net/recipes/)

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

## Описание проекта
Foodgram - продуктовый помощник с базой кулинарных рецептов. Позволяет
публиковать рецепты, сохранять избранные, а также формировать список покупок
для выбранных рецептов. Можно подписываться на любимых авторов.

В проекте применена технология контейнеризации Docker. Проект состоит из
сервисов, которые запакованы в отдельные контейнеры: Django-приложение, база
данных Postgres, серверы Gunicorn и Nginx. Образ проекта находится на
DockerHub, скачать его можно командой:
```
sudo docker pull vandruhav/foodgram:v1
```

## Шаблон env-файла
- SECRET_KEY - ключ к защите подписанных данных
- DEBUG - ключ отладки приложения
- ALLOWED_HOSTS - список хостов/доменов, для которых может работать проект
- DB_ENGINE - используемый движок для доступа к БД
- DB_NAME - имя БД
- POSTGRES_USER - логин для подключения к БД
- POSTGRES_PASSWORD - пароль для подключения к БД
- DB_HOST - название сервиса (контейнера)
- DB_PORT - порт для подключения к БД

## Установка приложения
На вашем компьютере должны быть установлены Docker и надстройка Docker-compose.
1. Склонируйте репозиторий YaMDb с GitHub.com:
```
git clone git@github.com:vandruhav/infra_sp2.git
```
2. Перейдите в директорию:
```
cd infra_sp2/infra
```
3. Соберите контейнеры и запустите их:
```
sudo docker-compose up -d
```
4. Выполните миграции в контейнере web:
```
sudo docker-compose exec web python manage.py migrate
```
5. Создайте суперпользователя в контейнере web:
```
sudo docker-compose exec web python manage.py createsuperuser
```
6. Соберите статику в контейнере web:
```
sudo docker-compose exec web python manage.py collectstatic --no-input
```
6. Проект доступен, все функции и эндпойнты описаны в документации:
```
http://localhost/redoc/
```

## Заполнение базы данных
Для заполнения БД данными, предоставленными с проектом, используйте команду:
```
sudo docker-compose exec web python manage.py fill_db
```

## Регистрации пользователей
- Пользователь отправляет POST-запрос на добавление нового пользователя с
параметрами "email" и "username" на эндпойнт "/api/v1/auth/signup/"
- YaMDB отправляет письмо с кодом подтверждения на адрес email.
- Пользователь отправляет POST-запрос с параметрами "username" и
"confirmation_code" на эндпойнт "/api/v1/auth/token/", в ответе на запрос ему
приходит JWT-токен.
- При желании пользователь отправляет PATCH-запрос на эндпойнт
"/api/v1/users/me/" и заполняет поля в своём профайле (описание полей — в
документации).

#
(с) Дипломная работа Воробьёва Андрея.
