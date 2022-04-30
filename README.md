![example event parameter](https://github.com/plngu/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?event=push)
# api_yamdb
Проект YaMDb собирает отзывы пользователей на произведения

### Возможности:

- Запросы от пользователей с различными ролями: анонимный пользователь, зарегистрированный пользователь, модератор, администратор;
- Пользователи могут создавать и редактировать отзывы и оценивать произведения, на основе оценок пользователей рассчитывается средний рейтинг произведения;
- Аутентификация по JWT-токену.

Примеры доступных энедпоинтов [ReDoc](https://redocly.github.io/redoc/#operation/addPet):

```
http://51.250.97.177/admin/
http://51.250.97.177/redoc/
```

### Установка (Windows):

Клонировать репозиторий:

```
git clone https://github.com/plngu/api_yamdb_final.git
cd api_yamdb_final
```

Создать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```


Загрузить зависимости из requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py makemigrations
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

Разработчик проекта
Алексей Панченко

E-mail: j66k@yandex.ru

Github: https://github.com/plngu/
