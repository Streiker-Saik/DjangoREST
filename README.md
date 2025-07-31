# Проект "API с помощью Django"

## Содержание:
- [Описание](#описание)
- [Проверить версию Python](#проверить-версию-python)
- [Установка Poetry](#установка-poetry)
- [Установка](#установка)
- [Запуск проекта](#запуск-проекта)
- [Структура проекта](#структура-проекта)
- [Приложение lms](#приложение-lms)
  - [Models lms](#models-lms)
    - [Course](#course)
    - [Lesson](#lesson)
  - [Serializers lms](#serializers-lms)
  - [Urls lms](#urls-lms)
  - [Views lms](#views-lms)
- [Приложение users](#приложение-users)
  - [Models users](#models-users)
    - [User](#user)
  - [Serializers lms](#serializers-users)
  - [Urls lms](#urls-users)
  - [Views lms](#views-users)



## Описание:

Разработка приложения(веб-сайта) онлайн магазина и блога, с помощью фреймворка Django.

[<- на начало](#содержание)

## Проверить версию Python:

Убедитесь, что у вас установлен Python (версия 3.x). Вы можете проверить установленную версию Python, выполнив команду:
```
python --version
```

[<- на начало](#содержание)

## Установка Poetry:
Если у вас еще не установлен Poetry, вы можете установить его, выполнив следующую команду
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
Проверить Poetry добавлен в ваш PATH.
```bash
poetry --version
```

[<- на начало](#содержание)

## Установка:
- Клонируйте репозиторий:
```bash
git clone git@github.com:Streiker-Saik/DjangoREST.git
```
- Перейдите в директорию проекта:
```
cd DjangoREST
```
### При использовании PIP:
- Активируйте виртуальное окружение
```
python -m venv <имя_вашего окружения>
<имя_вашего_окружения>\Scripts\activate
```
- Установите зависимости
```
pip install -r requirements.txt
```
### При использование POETRY:
- Активируйте виртуальное окружение
```bash
poetry shell
```
- Установите необходимые зависимости:
```bash
poetry install
```
или
```bash
poetry add django python-dotenv psycopg2 pillow djangorestframework
poetry add --group lint flake8 black isort mypy==1.16.0
```
- Зайдите в файл .env.example и следуйте инструкция

[<- на начало](#содержание)

## Запуск проекта:
Чтобы запустить сервер разработки, выполните следующую команду:
```bash
python manage.py runserver
```

## Структура проекта:
```
DjangoREST/
├── config/
|   ├── __init__.py
|   ├── asgi.py
|   ├── settings.py # настройки проекта
|   ├── urls.py # маршрутизация проета
|   └── wsgi.py
├── lms/ # приложение lms-система
|   ├── migrations/ # пакет миграции моделей
|   |   ├── 0001_initial.py
|   |   └── __init__.py
|   ├── admin.py 
|   ├── apps.py
|   ├── models.py # модели БД
|   ├── seriazers.py # сериализаторы приложения
|   ├── tests.py 
|   ├── urls.py # маршрутизация приложения
|   └── views.py # конструктор контроллеров
├── users/ # приложение аутефикации
|   ├── migrations/ # пакет миграции моделей
|   |   ├── 0001_initial.py
|   |   └── __init__.py
|   ├── admin.py 
|   ├── apps.py
|   ├── models.py # модели БД
|   ├── seriazers.py # сериализаторы приложения
|   ├── tests.py 
|   ├── urls.py # маршрутизация приложения
|   └── views.py # конструктор контроллеров
├── .env
├── .flake8 # настройка для flake8
├── .gitignore
├── poetry.lock
├── pypproject.toml # зависимости для poetry
├── README.md
└── requirements.txt # зависимости для pip
```

[<- на начало](#содержание)

---
# Приложение lms:

---
## Models lms
### Course:
Представление курса
Атрибуты:
- title(str): Название курса
- preview(ImageField): Превью курса
- description(str): Описание курса
### Lesson:
Представление урока
Атрибуты:
- title(str): Название урока
- description(str): Описание урока
- preview(ImageField): Превью урока
- video_url(URLField): Ссылка на видео
- courses(ForeignKey): Курс (внешний ключ на модель Course(Курс))

[<- на начало](#содержание)

---
## Serializers lms:
### CourseSerializer:
Сериализатор для модели Course.
Показывает все поля.
### LessonSerializer:
Сериализатор для модели Lesson.
Показывает все поля.

[<- на начало](#содержание)

---
## Urls lms:
- Список курсов (доступны методы: **GET/POST**)
  http://127.0.0.1:8000/courses/
- Получение урока (доступны методы: **GET/PUT/PATH/DELETE**)
  http://127.0.0.1:8000/courses/(pk)/
  - где (pk) - это, целое число PrimaryKey, ID курса
- Список уроков (доступны методы: **GET**)
  http://127.0.0.1:8000/courses/lessons/
- Создание урока (доступны методы: **POST**)
  http://127.0.0.1:8000/courses/lessons/create/
- Получение одного урока (доступны методы: **GET**)
  http://127.0.0.1:8000/courses/lessons/(pk)/
  - где (pk) - это, целое число PrimaryKey, ID урока
- Редактирование урока (доступны методы: **PUT/PATH**)
  http://127.0.0.1:8000/courses/lessons/(pk)/update/
  - где (pk) - это, целое число PrimaryKey, ID урока
- Удаление урока (доступны методы: **DELETE**)
  http://127.0.0.1:8000/courses/lessons/(pk)/delete/
  - где (pk) - это, целое число PrimaryKey, ID урока

[<- на начало](#содержание)

---
## Views lms:
### CourseViewSet:
Представление набора действий для модели Course.  
Позволяет выполнять операции с курсами:
отображение списка, создание, отображение, полное обновление, частичное обновление, удаление.
### LessonCreateAPIView:
Представление для создания нового урока (POST)
### LessonListAPIView:
Представление для получения списка всех уроков (GET)
### LessonRetrieveAPIView:
Представление для получения урока по идентификатору (GET)
### LessonUpdateAPIView:
Представление для обновления урока по идентификатору (PUT/PATH)
### LessonDestroyAPIView:
Представление для удаления урока по идентификатору (DELETE)

[<- на начало](#содержание)

---

# Приложение users:

---
## Models users
### User:
Представление кастомного пользователя, расширяющее AbstractUser.
Поле авторизации с username изменено на email. Так же username обязательное поле при авторизации
Атрибуты:
- username: Логин **отключен**
- email(str): Уникальный email
- phone_number(str): Номер телефона
- city(str): Город
- avatar(ImageField): Аватар (изображение)

[<- на начало](#содержание)

---
## Serializers users:
### UserSerializer:
Сериализатор для модели User.
Показывает поля: id, first_name, last_name, phone_number, city

[<- на начало](#содержание)

---
## Urls lms:
- Список пользователей (доступны методы: **GET**)
  http://127.0.0.1:8000/users/
- Получение одного пользователя (доступны методы: **GET**)
  http://127.0.0.1:8000/users/(pk)/
  - где (pk) - это, целое число PrimaryKey, ID пользователя
- Редактирование пользователя (доступны методы: **PUT/PATH**)
  http://127.0.0.1:8000/users/(pk)/update/
  - где (pk) - это, целое число PrimaryKey, ID пользователя

[<- на начало](#содержание)

---
## Views users:
### UserListAPIView:
Представление для получения списка всех пользователей (GET)
### UserRetrieveAPIView:
Представление для получения пользователя по идентификатору (GET)
### UserUpdateAPIView:
Представление для обновления пользователя по идентификатору (PUT/PATH)

[<- на начало](#содержание)

---