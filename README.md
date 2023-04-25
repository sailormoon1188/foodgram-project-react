
<a id="anchor"></a>

![workflow](https://github.com/sailormoon2111/foodgram-project-react/actions/workflows/main.yml/badge.svg?event=push)

### Продуктовый помощник **Foodgram** 
_Для обмена кулинарными рецептами любимых блюд._

Дипломный проект студентки _Яндекс.Практикум_ по курсу **"Python-разработчик"**

**Описание**
«Продуктовый помощник»: приложение, на котором пользователи публикуют рецепты кулинарных изделий, подписываться на публикации других авторов и добавлять рецепты в свое избранное. Сервис «Список покупок» позволит пользователю создавать список продуктов, которые нужно купить для приготовления выбранных блюд согласно рецепта/ов.

**API для сервиса YaMDb.** позволяет работать со следующими сущностями:

**Пользователи** (Получить список всех пользователей, создание пользователя, получить пользователя по username, изменить данные пользователя по username, удалить пользователя по username, получить данные своей учетной записи, изменить данные своей учетной записи)

**Тэги**, которые создаются администратором для добавления к рецептам, для удобного поиска и навигации среди рецептов

**Ингредиенты** предустановлен основной набор ингредиентов, возможно добавление новых ингредиентов авторизованными пользователями 

**Рецепты** Основная сущность - посты с рецептами авторизованных пользователей

**Избранное** Можно добавить/удалить рецепт в/из избранное

**Подписки** реализована возможность подписаться на аторов рецепта

**Токен (Djoser)** для поьзователей АПИ реализована аторизация по токену. 

**После запуска проекта ознакомиться с документацией можно по ссылке** http://localhost/api/docs/

**АПИ. Примеры запросов и ответов (в формате json)**
Получить токен:
POST: http://localhost/api/auth/token/login/
~~~
{
  "password": "string",
  "email": "string"
}
~~~
 Регистрация нового пользователя:
POST: http://localhost/api/users/
~~~
{
  "email": "vpupkin@yandex.ru",
  "username": "vasya.pupkin",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "password": "Qwerty123"
}
~~~
Изменение пароля:
POST: http://localhost/api/users/set_password/
~~~
{
  "new_password": "string",
  "current_password": "string"
}
~~~
Получение списка всех рецептов с пагинацией (токен не требуется):
GET: http://localhost/api/recipes/
~~~
{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {}
  ]
}
~~~
Получение списка всех тегов (токен не требуется):
GET: http://localhost/api/tags/
~~~
[
  {
    "id": 0,
    "name": "Завтрак",
    "color": "#E26C2D",
    "slug": "breakfast"
  }
]
~~~
Получить информацию о рецепте по id(токен не требуется):
GET: http://localhost/api/recipes/{id}/
~~~
{
  "id": 0,
  "tags": [
    {}
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
  },
  "ingredients": [
    {}
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}
~~~
Получить инфо об определенном ингредлиенте :
GET: http://localhost/api/ingredients/{id}/
{
  "id": 0,
  "name": "Капуста",
  "measurement_unit": "кг"
}
~~~
Авторизованные пользователи могут добавлять / удалять рецепты из избранного, удалять и редактировать свои подписки на других авторов. Для этого необходимо сделать POST или DELETE запросы 
Также им доступны все действия с рецептами, авторами которых они являются. 

Добавить рецепт в избранное :
GET:http://localhost/api/recipes/{id}/favorite/
{
  "id": 0,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "cooking_time": 1
}
~~~
Подписаться на другого автора:
GET: http://localhost/api/users/{id}/subscribe/
~~~
{
  "email": "user@example.com",
  "id": 0,
  "username": "string",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "is_subscribed": true,
  "recipes": [
    {}
  ],
  "recipes_count": 0
}
~~~

Загрузить список покупок для приготовления любимого рецепта:
GET: http://localhost/api/recipes/download_shopping_cart/
~~~
{
  "detail": "Учетные данные не были предоставлены."
}
~~~

**Используемый стек технологий:**

* язык программирования Python 3.7.9 https://www.python.org/downloads/release/python-379/;
* фреймворк Django REST Framework 3.12.4 https://www.django-rest-framework.org/.
* аутентификация пользователей с помощью Djoser 2.1.0 https://djoser.readthedocs.io/en/latest/introduction.html

Инфраструктура: 
* Docker
* NGINX
* GUNICORN
* база даннных POSTGRES

**Запуск проекта**
Клонируйте проект 

~~~
git clone git@hgithub.com/sailormoon2111/foodgram-project-react
~~~

При первом запуске для функционирования проекта обязательно установить виртуальное окружение, установить зависимости,  выполнить миграции:
```
# создаем виртуальное окружение
python -m venv env

source venv/Scripts/activate
```
```
# далее переходим в директорию backend
python -m pip install --upgrade pip

pip install -r requirements.txt
```
Установить и запустить приложения в контейнерах:

```
# переходим в infra файлом docker-compose.yaml и запускаем контейнеры
docker-compose up -d --build
```
```
# далее выполняем миграции
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```
```
#Создаем суперпользователя:
docker-compose exec backend python manage.py createsuperuser
```
```
#Создаем ингредиенты из CSV файла:

docker-compose exec backend python manage.py add-ingredients

#Сoрбираем статику:
docker-compose exec backend python manage.py collectstatic --no-input
```
```
#Создаем дамп базы данных :
docker-compose exec backend python manage.py dumpdata > dump.json
```
```
# загрузка фикстур в базу данных
docker cp dump.json <container id>:app/

# далее 
docker-compose exec backend python manage.py loaddata dump.json
```
```
#Остановить контейнеры:
docker-compose down -v
```

_Шаблон наполнения env-файла_

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=
DEBUG=False
```
***IP адресс проекта: 62.84.118.240***

**Контакты**


[Ванданова Мария.](https://github.com/sailormoon2111)
backend. API. Сборка образа. Деплой. 


_[Вверх](#anchor)_