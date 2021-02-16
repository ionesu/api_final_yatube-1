# API для Yatube
Программный интерфейс для социальной сети блогеров. Реализован CRUD доступ к публикациям и комментариям, а также доступ для создания объекта и для получения списка объектов к подпискам и группам. Авторизация через JWT-токен. 

### Подготовка тестовой базы данных перед первым запуском проекта:
* выполнить миграции командой `python manage.py migrate`
* создать суперпользователя командой `python manage.py createsuperuser`
* (опционально) заполнить базу тестовыми данными командой `python manage.py loaddata fixtures.json`

### Примеры локальных запросов:
| Путь  | Метод | Описание |
| ------- | ---------| ---------|
| http://127.0.0.1:8000/api/v1/token/ | POST | Получить JWT-токен |
| http://127.0.0.1:8000/api/v1/posts/ | GET | Получить список всех публикаций |
| http://127.0.0.1:8000/api/v1/posts/ | POST | Создать новую публикацию |
| http://127.0.0.1:8000/api/v1/posts/{id}/ | GET | Получить публикацию по id |
| http://127.0.0.1:8000/api/v1/posts/{id}/ | PUT | Обновить публикацию по id |
| http://127.0.0.1:8000/api/v1/posts/{id}/ | PATCH | Частично обновить публикацию по id |
| http://127.0.0.1:8000/api/v1/posts/{id}/ | DELETE | Удалить публикацию по id |

Локальный адрес полной документации http://127.0.0.1:8000/redoc/

### Технологии
* [Python](https://www.python.org/) версия 3.8.5
* [Django Framework](https://www.djangoproject.com/) версия 3.1.6
* [Django Rest Framework](https://www.django-rest-framework.org/) версия 3.12.2

### Автор:
[Dmitriy Peretoka](https://github.com/dmitriyperetoka)
