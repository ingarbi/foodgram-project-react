# Foodgram «Продуктовый помощник»



## Описание:

Веб-приложение Foodgram, «Продуктовый помощник». На сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Стек технологий:
* Python 
* Django 
* DjangoRestFramework 
* PostgresSQL 
* Nginx
* Docker, Docker-compose, DockerHub

## Запуск проекта локально:

1. Клонируйте репозиторий проекта с GitHub:
```
git clone git@github.com:ingarbi/foodgram-project-react.git
```

2. В терминале, перейдите в каталог: 
```
cd .../foodgram-project-react/infra
```

и создайте там файл .evn для хранения ключей:
```
DEBUG_STATUS = False, еcли планируете использовать проект для разработки укажите  True
SECRET_KEY = 'секретный ключ Django проекта'
DB_ENGINE=django.db.backends.postgresql # указываем, что используем postgresql
DB_NAME=postgres # указываем имя созданной базы данных
POSTGRES_USER=postgres # указываем имя своего пользователя для подключения к БД
POSTGRES_PASSWORD=postgres # устанавливаем свой пароль для подключения к БД
DB_HOST=db # указываем название сервиса (контейнера)
DB_PORT=5432 # указываем порт для подключения к БД 
```

3. Запустите окружение:

* Запустите docker-compose, развёртывание контейнеров выполниться в «фоновом режиме»
```
docker-compose up
```

* выполните миграции:
```
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```

*  соберите статику:
```
docker-compose exec backend python manage.py collectstatic --no-input
```

* cоздайте суперпользователя, введите - почту, логин, пароль:
```
docker-compose exec backend python manage.py createsuperuser
```

*  загрузите в базу список ингридиентов и тэгов:
```
docker-compose exec backend python manage.py load_ingredients
docker-compose exec backend python manage.py load_tags
```
### Проект готов к работе

Backend проекта выполнил студент 56 когорты Яндекс Практикума  
Arby Sayid-Ibrakhimi
https://github.com/ingarbi
