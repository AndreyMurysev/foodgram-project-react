# Сайт с рецептами
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)
[![Django-app workflow](https://github.com/AndreyMurysev/foodgram-project-react/actions/workflows/main.yml/badge.svg)]

## Описание:

Cайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. 
Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

## Для работы с сайтом

### Учетные данные администратора:
email: admin@mail.ru  
password: admin  

### Основные адреса: 

| Адрес | Описание |
|:----------------|:---------|
| 51.250.28.118 | Главная страница |
| 51.250.28.118/admin/ | Для входа в панель администратора |
| 51.250.28.118/api/docs/ | Описание работы API |

## Пользовательские роли
| Функционал | Авторизованные пользователи |  Неавторизованные пользователи | Администратор  |
|:----------------|:---------:|:---------:|:---------:|
| Доступна главная страница. | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна и работает форма авторизации | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна главная страница | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна страница отдельного рецепта. | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна страница «Мои подписки» | :heavy_check_mark: | :x: | :heavy_check_mark: |
| Можно подписаться и отписаться на странице рецепта | :heavy_check_mark: | :x: | :heavy_check_mark: |
| Можно подписаться и отписаться на странице автора | :heavy_check_mark: | :x: | :heavy_check_mark: |
| При подписке рецепты автора добавляются на страницу «Мои подписки» и удаляются оттуда при отказе от подписки. | :heavy_check_mark: | :x: | :heavy_check_mark: |
| Доступна страница «Избранное» | :heavy_check_mark: | :x: | :heavy_check_mark: |
| На странице рецепта есть возможность добавить рецепт в список избранного и удалить его оттуда | :heavy_check_mark: | :x: | :heavy_check_mark: |
| На любой странице со списком рецептов есть возможность добавить рецепт в список избранного и удалить его оттуда | :heavy_check_mark: | :x: | :heavy_check_mark: |
| Доступна страница «Список покупок» | :heavy_check_mark: | :x: | :heavy_check_mark: |
| На странице рецепта есть возможность добавить рецепт в список покупок и удалить его оттуда | :heavy_check_mark: | :x: | :heavy_check_mark: |
| На любой странице со списком рецептов есть возможность добавить рецепт в список покупок и удалить его оттуда | :heavy_check_mark: | :x: | :heavy_check_mark: |
| Есть возможность выгрузить файл (.txt или .pdf) с перечнем и количеством необходимых ингредиентов для рецептов из «Списка покупок» | :heavy_check_mark: | :x: | :heavy_check_mark: |
| Ингредиенты в выгружаемом списке не повторяются, корректно подсчитывается общее количество для каждого ингредиента | :heavy_check_mark: | :x: | :heavy_check_mark: |
| Доступна страница «Создать рецепт» | :heavy_check_mark: | :x: | :heavy_check_mark: |
| Есть возможность опубликовать свой рецепт | :heavy_check_mark: | :x: | :heavy_check_mark: |
| Есть возможность отредактировать и сохранить изменения в своём рецепте | :heavy_check_mark: | :x: | :heavy_check_mark: |
| Есть возможность удалить свой рецепт | :heavy_check_mark: | :x: | :heavy_check_mark: |
| Доступна и работает форма изменения пароля | :heavy_check_mark: | :x: | :heavy_check_mark: |
| Доступна возможность выйти из системы (разлогиниться) | :heavy_check_mark: | :x: | :heavy_check_mark: |
| Доступна и работает система восстановления пароля. | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна и работает форма регистрации. | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |


## Администратор и админ-зона
:one: Все модели выведены в админ-зону.
:two: Для модели пользователей включена фильтрация по имени и email.
:three: Для модели рецептов включена фильтрация по названию, автору и тегам.
:four: На админ-странице рецепта отображается общее число добавлений этого рецепта в избранное.
:five: Для модели ингредиентов включена фильтрация по названию.

## Создание пользователя администратором
Пользователя может создать администратор — через админ-зону сайта или через POST-запрос на специальный эндпоинт api/users/ (описание полей 
запроса для этого случая — в документации).  Далее пользователь отправляет POST-запрос с параметрами email и password на эндпоинт /api/auth/token/, 
в ответе на запрос ему приходит token, как и при самостоятельной регистрации.

## Шаблон наполнения env-файла

```
EMAIL_HOST_USER=mail@mail.ru
EMAIL_HOST_PASSWORD=gsdlfghl
SECRET_KEY=p&l%385148kl9(vs
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
ALLOWED_HOSTS='*'

```
## Запуск проекта

- Клонировать репозиторий GitHub (не забываем создать виртуальное окружение и установить зависимости):
[https://github.com/AndreyMurysev/foodgram-project-react/](https://github.com/AndreyMurysev/foodgram-project-react/)

- Создать файл .env в папке проекта:
```
EMAIL_HOST_USER=mail@mail.ru
EMAIL_HOST_PASSWORD=gsdlfghl
SECRET_KEY=p&l%385148kl9(vs
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
ALLOWED_HOSTS='*'
```

- в Docker cоздаем образ :

```
docker build -t foodgram .
```
- Собираем контейнеры:
```
docker-compose up -d
```
В результате должны быть собрано три контейнер, при введении следующей команды:
```
docker ps
```
получаем список запущенных контейнеров:
_Пример:_

```
CONTAINER ID   IMAGE                             COMMAND                  CREATED       STATUS       PORTS                               NAMES
ffbe984f7533   nginx:1.19.3                      "/docker-entrypoint.…"   3 weeks ago   Up 3 weeks   0.0.0.0:80->80/tcp, :::80->80/tcp   andrey_murysev_nginx_1
5166bcfb1188   andreymurysev/mysite_fod:latest   "/bin/sh -c 'gunicor…"   3 weeks ago   Up 3 weeks                                       andrey_murysev_web_1
a9c7a7542ddb   postgres:12.4                     "docker-entrypoint.s…"   3 weeks ago   Up 3 weeks   5432/tcp                            andrey_murysev_db_1
```

| IMAGES | NAMES | DESCRIPTIONS
|:----------------:|:---------|:---------:|
| nginx:1.19.3 | andrey_murysev_nginx_1 | контейнер HTTP-сервера |
| postgres:12.4 | andrey_murysev_web_1 | контейнер базы данных |
| andreymurysev/mysite_fod:latest  | andrey_murysev_db_1 | контейнер приложения Django|


- Сделать миграции, создать суперпользователя и собрать статику:
```
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input 
```

- Для переноса данных с файла fixtures.json на PostgreSQL выполним несколько команд:
    ```
    docker-compose exec web python manage.py shell 
    ```
    Выполнить в открывшемся терминале:
    ```
    >>> from django.contrib.contenttypes.models import ContentType
    >>> ContentType.objects.all().delete()
    >>> quit()
    ```
    ```
    docker-compose exec web python manage.py loaddata dump.json
    ```
### Автор проекта:
_Мурысев Андрей_
**email:** _andreimurysev@yandex.ru_
**telegram:** _@andrey_murysev_

  
