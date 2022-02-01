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

## Описание:

Cайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. 
Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

## Для работы с сайтом

### Учетные данные администратора:
email: admin@mail.ru  
password: admin  

### Основные адреса: 

| Адрес | Описание |
|:----------------|:---------:|
| 51.250.28.118 | Сайт |
| 51.250.28.118/admin/ | Для входа в панель администратора |
| 51.250.28.118/api/docs/ | Описание работы API |


## Пользовательские роли
Для авторизованных пользователей:
- Доступна главная страница.
- Доступна страница другого пользователя.
- Доступна страница отдельного рецепта.
- Доступна страница «Мои подписки».
    1. Можно подписаться и отписаться на странице рецепта.
    2. Можно подписаться и отписаться на странице автора.
    3. При подписке рецепты автора добавляются на страницу «Мои подписки» и удаляются оттуда при отказе от подписки.
- Доступна страница «Избранное».
    1. На странице рецепта есть возможность добавить рецепт в список избранного и удалить его оттуда.
    2. На любой странице со списком рецептов есть возможность добавить рецепт в список избранного и удалить его оттуда.
- Доступна страница «Список покупок».
    1. На странице рецепта есть возможность добавить рецепт в список покупок и удалить его оттуда.
    2. На любой странице со списком рецептов есть возможность добавить рецепт в список покупок и удалить его оттуда.
    3. Есть возможность выгрузить файл (.txt или .pdf) с перечнем и количеством необходимых ингредиентов для рецептов из «Списка покупок».
    4. Ингредиенты в выгружаемом списке не повторяются, корректно подсчитывается общее количество для каждого ингредиента.
- Доступна страница «Создать рецепт».
  1. Есть возможность опубликовать свой рецепт.
  2. Есть возможность отредактировать и сохранить изменения в своём рецепте.
  3. Есть возможность удалить свой рецепт.
- Доступна и работает форма изменения пароля.
- Доступна возможность выйти из системы (разлогиниться).
Для неавторизованных пользователей
- Доступна главная страница.
- Доступна страница отдельного рецепта.
- Доступна страница любого пользователя.
- Доступна и работает форма авторизации.
- Доступна и работает система восстановления пароля.
- Доступна и работает форма регистрации.
Администратор и админ-зона
- Все модели выведены в админ-зону.
- Для модели пользователей включена фильтрация по имени и email.
- Для модели рецептов включена фильтрация по названию, автору и тегам.
- На админ-странице рецепта отображается общее число добавлений этого рецепта в избранное.
- Для модели ингредиентов включена фильтрация по названию.

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
## Описание команд для запуска приложения в контейнерах

Создаем образ:
```
docker build -t foodgram .
```
Собираем контейнеры:
```
docker-compose up -d
```
Создаем файлы миграции:
```
docker-compose exec web python manage.py makemigrations
```
```
docker-compose exec web python manage.py migrate
```
Создаем администратора:

```
docker-compose exec web python manage.py createsuperuser
```
Собираем файлы статики:
```
docker-compose exec web python manage.py collectstatic --no-input 
```

## Описание команды для заполнения базы данными
Для переноса данных с файла fixtures.json на PostgreSQL выполним несколько команд:
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
## Технологии
- Python
- Django 
- Docker
- postgresql
- nginx
- gunicorn

[![Django-app workflow](https://github.com/AndreyMurysev/foodgram-project-react/actions/workflows/main.yml/badge.svg)]


  
