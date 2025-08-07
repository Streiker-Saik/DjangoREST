# Проект "API с помощью Django"

## Содержание:
- [Описание](#описание)
- [Проверить версию Python](#проверить-версию-python)
- [Установка Poetry](#установка-poetry)
- [Установка](#установка)
- [Запуск проекта](#запуск-проекта)
- [Кастомные команды](#кастомные-команды)
- [Структура проекта](#структура-проекта)
- [Приложение lms](#приложение-lms)
  - [Models lms](#models-lms)
    - [Course](#course)
    - [Lesson](#lesson)
    - [Subscription](#subscription)
  - [Paginators lms](#paginators-lms)
  - [Serializers lms](#serializers-lms)
  - [Urls lms](#urls-lms)
  - [Validators lms](#validators-lms)
  - [Views lms](#views-lms)
- [Приложение users](#приложение-users)
  - [Admin users](#admin-users)
  - [Models users](#models-users)
    - [User](#user)
  - [Permissions users](#permissions-users)
  - [Serializers user](#serializers-users)
  - [Urls user](#urls-users)
  - [Views user](#views-users)


## Описание:

Разработка приложения(веб-сайта) онлайн магазина и блога, с помощью фреймворка Django.

[<- на начало](#содержание)

---
## Проверить версию Python:

Убедитесь, что у вас установлен Python (версия 3.x). Вы можете проверить установленную версию Python, выполнив команду:
```
python --version
```

[<- на начало](#содержание)

---
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

---
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
poetry add django python-dotenv psycopg2 pillow djangorestframework django-filter djangorestframework_simplejwt
poetry add --group lint flake8 black isort mypy==1.16.0
```
- Зайдите в файл .env.example и следуйте инструкция

[<- на начало](#содержание)

---
## Запуск проекта:
Чтобы запустить сервер разработки, выполните следующую команду:
```bash
python manage.py runserver
```

[<- на начало](#содержание)

---
## Кастомные команды
### add_groups
Команда для добавления групп из fixture
- 'group_fixture.json'
```bash
python manage.py add_groups
```
### csu
Команда для создания суперпользователя по ключам email и password.
Если не указано, то: email='admin@example.com', password='admin'.
```bash
python manage.py csu
```
или
```
python manage.py csu --email ввести_адрес_почты --password ввести_пароль
```
### add_test_data_lms
Команда для добавления тестовых данных(курсы, уроки) из fixture
- 'lms/fixture/course_fixture.json'
- 'lms/fixture/lesson_fixture.json
```bash
python manage.py add_test_data_lms
```
### add_test_data_users
Команда для добавления тестовых данных(курсы, уроки) из fixture
- 'users/fixture/user_fixture.json'
- 'users/fixture/payment_fixture.json
```bash
python manage.py add_test_data_users
```

[<- на начало](#содержание)

---
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
|   ├── fixture/ # фикстуры
|   |   └── ...
|   ├── management/
|   |   └── commands
|   |   |   ├── add_test_data_lms.py # команда заполнения тестовыми данными БД
|   |   |   └── __init__.py
|   |   └── __init__.py
|   ├── migrations/ # пакет миграции моделей
|   |   ├── 0001_initial.py
|   |   ├── ...
|   |   └── __init__.py
|   ├── admin.py 
|   ├── apps.py
|   ├── models.py # модели БД
|   ├── paginators.py # 
|   ├── seriazers.py # сериализаторы приложения
|   ├── tests.py 
|   ├── urls.py # маршрутизация приложения
|   ├── validators # валидаторы сериализаторов
|   └── views.py # конструктор контроллеров
├── users/ # приложение аутефикации
|   ├── management/
|   |   └── commands
|   |   |   ├── csu.py # Создание суперюзера
|   |   |   ├── create_user.py # Создание пользователя
|   |   |   ├── add_test_data_users.py # команда заполнения тестовыми данными БД
|   |   |   └── __init__.py
|   |   └── __init__.py
|   ├── migrations/ # пакет миграции моделей
|   |   ├── 0001_initial.py
|   |   ├── ...
|   |   └── __init__.py
|   ├── admin.py 
|   ├── apps.py
|   ├── models.py # модели БД
|   ├── permissions.py # правв доступа
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
- Атрибуты:
  - title(str): Название курса
  - preview(ImageField): Превью курса
  - description(str): Описание курса
  - owner(ForeignKey): Владелец (внешний ключ на модель User(Пользователь))
### Lesson:
Представление урока
- Атрибуты:
  - title(str): Название урока
  - description(str): Описание урока
  - preview(ImageField): Превью урока
  - video_url(URLField): Ссылка на видео
  - courses(ForeignKey): Курс (внешний ключ на модель Course(Курс))
  - owner(ForeignKey): Владелец (внешний ключ на модель User(Пользователь))
### Subscription:
Представление подписки
- Атрибуты:
  - user(ForeignKey): Пользователь (внешний ключ на модель User(Пользователь))
  - course(ForeignKey): Курс (внешний ключ на модель Course(Курс))

[<- на начало](#содержание)
---
## Paginators lms:
### LmsPaginator:
Пагинатор для приложения lms. 
К-во элементов 3 (максимум 10) на странице

[<- на начало](#содержание)

---
## Serializers lms:
### CourseSerializer:
Сериализатор для модели Course
- Отображаются поля:
  - id(int): Уникальный идентификатор курса.
  - count_lessons(int): Количество уроков в курсе
  - lessons(list): Список уроков (LessonSerializer)
  - title(str): Название курса.
  - preview(ImageField): Превью курса.
  - description(str): Описание курса.
  - is_subscribed(bool): Если подписка у пользователя
- Методы:
  - get_count_lessons(self, obj) -> int: Получение количества уроков в курсе
  - get_is_subscribed(self, obj) -> bool: Есть ли подписка у пользователя
### LessonSerializer:
Сериализатор для модели Lesson
- Отображаются поля:
  - id(int): Уникальный идентификатор урока.
  - title(str): Название урока.
  - description(str): Описание урока.
  - preview(ImageField): Превью урока.
  - video_url(URLField): Ссылка на видео урока.
  - courses(ForeignKey): Внешний ключ на курс.

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
- Добавление/удаление подписки на курс (доступны методы: **POST**)
  http://127.0.0.1:8000/courses/manger_subscribe/
  запрос: {"course_id": <id_курса> }

[<- на начало](#содержание)

---
## Validators lms:
### DescriptionValidator
Валидатор проверки описания на наличие ссылок.
Проверяет значение на наличие ссылок кроме YouTube.
### UrlValidator
Валидатор url ссылки.
Проверяет значение на соответствие формату ссылки видео на YouTube.

[<- на начало](#содержание)

---
## Views lms:
### CourseViewSet:
Представление набора действий для модели Course.  
Позволяет выполнять операции с курсами:
отображение списка, создание, отображение, полное обновление, частичное обновление, удаление.
- Методы:
  - get_queryset(self) -> QuerySet: **!временно отключена!**   
  Возвращает список уроков, к которым у пользователя есть доступ.
  Если пользователь является модератором, возвращает все уроки.
  В противном случае, возвращает только уроки, принадлежащие пользователю
  - get_permissions(self) -> list:  
  Определяет права доступа для различных действий:
    - создание - авторизованные пользователи не являющиеся модераторами
    - просмотр/изменение - авторизованные пользователи: модераторы и владельцы
    - удаление - авторизованные пользователи: владельцы
  - perform_create(self, serializer) -> None:  
  Сохраняет новый урок с текущим пользователем как владельцем.
### ManageSubscriptionAPIView:
Представление для создания/удаления подписки
- Методы:
  - post(self, request: Request) -> Response:  
  Пост запрос на добавление(если подписки нет) или удаление подписки(если есть).
### LessonCreateAPIView:
Представление для создания нового урока (POST)
- Методы:
  - perform_create(self, serializer) -> None:  
  Сохраняет новый урок с текущим пользователем как владельцем.
- Доступ:
  - авторизованному пользователю не модератору
### LessonListAPIView:
Представление для получения списка всех уроков (GET)
- Методы:
  - get_queryset(self) -> QuerySet:  
  Возвращает список курсов, к которым у пользователя есть доступ.
  Если пользователь является модератором, возвращает все курсы.
  В противном случае, возвращает только курсы, принадлежащие пользователю.
- Доступ:
  - авторизованному пользователю
### LessonRetrieveAPIView:
Представление для получения урока по идентификатору (GET)
- Доступ:
  - авторизованному пользователю:
    - модератору
    - владельцу
### LessonUpdateAPIView:
Представление для обновления урока по идентификатору (PUT/PATH)
- Доступ:
  - авторизованному пользователю:
    - модератору
    - владельцу
### LessonDestroyAPIView:
Представление для удаления урока по идентификатору (DELETE)
- Доступ:
  - авторизованному пользователю:
    - не модератору
    - владельцу

[<- на начало](#содержание)

---

# Приложение users:
## Admin users
### CustomUserAdmin
Класс для работы администратора с пользователями
- Атрибуты:
  - ordering - сортировка по email
  - list_filter - фильтрация активный пользователь или нет
  - exclude - исключит поле пароля
  - list_display - выводит на экран: email, имя, фамилия, супер юзер, сотрудник, активный
  - search_fields - поиск по: email

[<- на начало](#содержание)

---
## Models users
### User:
Представление кастомного пользователя, расширяющее AbstractUser.
Поле авторизации с username изменено на email. Так же username обязательное поле при авторизации
- Атрибуты:
  - username: Логин **отключен**
  - email(str): Уникальный email
  - phone_number(str): Номер телефона
  - city(str): Город
  - avatar(ImageField): Аватар (изображение)
### Payment:
Представление платежа.  
- Атрибуты:
  - user(ForeignKey): Пользователь (внешний ключ на модель «Пользователя»)
  - date_pay(datetime): Дата платежа
  - course(ForeignKey): Курс (внешний ключ на модель «Курс»)
  - lesson(ForeignKey): Урок (внешний ключ на модель «Урок»)
  - amount(int): Сумма платежа
  - payment_method(str): Способ оплаты. Возможные значения:
    - cash - Наличные,
    - transfer - Перевод на счет

[<- на начало](#содержание)

---
## Permissions users:
### IsOwner:
Право владельцам
### IsProfileOwner:
Право владельца профиля
### IsModerator:
Право модератора

[<- на начало](#содержание)

---
## Serializers users:
### UserGeneralSerializer:
Сериализатор общей информации для модели Users.
- Показывает поля:
  - id(int): Уникальный идентификатор пользователя
  - email(str): Почта пользователя
  - city(str): Город пользователя.
### UserSerializer:
Сериализатор для модели Users.
- Показывает поля: 
  - id(int): Уникальный идентификатор пользователя.
  - first_name(str): Имя пользователя.
  - last_name(str): Фамилия пользователя
  - phone_number(str): Номер телефона пользователя.
  - city(str): Город пользователя.
  - payments(list): Список платежей (PaymentSerializer)
### UserCreateSerializer:
Сериализатор для создания модели Users.
- Показывает поля:
  - id(int): Уникальный идентификатор пользователя
  - email(str): Почта пользователя
  - phone_number(str): Номер телефона пользователя
  - сity(str): Город пользователя.
### PaymentSerializer:
Сериализатор для модели Payment.
- Показывает поля:
  - id(int): Уникальный идентификатор платежа.
  - date_pay(datetime): Дата платежа.
  - amount(str): Сумма платежа.
  - payment_method(str): Метод платежа.
  - user(ForeignKey): Внешний ключ на пользователя.
  - course(ForeignKey): Внешний ключ на курс.
  - lesson(ForeignKey): Внешний ключ на урок.

[<- на начало](#содержание)

---
## Urls users:
- Список пользователей (доступны методы: **GET**)
  http://127.0.0.1:8000/users/
- Получение токена пользователя (доступны методы: **POST**)  
  http://127.0.0.1:8000/users/token/
- Обновление токена пользователя (доступны методы: **POST**)  
  http://127.0.0.1:8000/users/token/refresh/
- Создание пользователя (доступны методы: **POST**)
  http://127.0.0.1:8000/users/register/
- Получение одного пользователя (доступны методы: **GET**)
  http://127.0.0.1:8000/users/(pk)/
  - где (pk) - это, целое число PrimaryKey, ID пользователя
- Редактирование пользователя (доступны методы: **PUT/PATH**)
  http://127.0.0.1:8000/users/(pk)/update/
  - где (pk) - это, целое число PrimaryKey, ID пользователя
- Удаление пользователя (доступны методы: **DELETE**)
  http://127.0.0.1:8000/users/(pk)/delete/
  - где (pk) - это, целое число PrimaryKey, ID пользователя
- Список платежей (доступны методы: **GET**)
  http://127.0.0.1:8000/users/payments/
  - Сортировка по дате  
    - http://127.0.0.1:8000/users/payments/?ordering=date_pay # по возрастанию  
    - http://127.0.0.1:8000/users/payments/?ordering=-date_pay # по убыванию
  - Фильтрации  
    http://127.0.0.1:8000/users/payments/?course=(pk)&lesson=(pk)&payment_method=(pm)
    - http://127.0.0.1:8000/users/payments/?course=(pk) # по курсу  
    где (pk) - это, целое число PrimaryKey, ID курса
    - http://127.0.0.1:8000/users/payments/?lesson=(pk) # по уроку  
    где (pk) - это, целое число PrimaryKey, ID урока
    - http://127.0.0.1:8000/users/payments/?payment_method=(pm) # по типу платежа  
    где (pm) - это тип платежа cash|transfer

[<- на начало](#содержание)

---
## Views users:
### UserListAPIView:
Представление для получения списка всех пользователей (GET)
- Методы:
  - get_serializer_class(self):  
  Определяет, какой сериализатор использовать для ответа.
  Возвращает UserSerializer для администраторов, а UserGeneralSerializer для обычных пользователей.
- Доступ:
  - авторизованному пользователю
### UserCreateAPIView:
Представление для создания пользователя (POST)
- Методы:
  - perform_create(self, serializer) -> None:  
  Сохраняет нового пользователя и устанавливает его активным.
- Доступ:
  - Всем
### UserRetrieveAPIView:
Представление для получения пользователя по идентификатору (GET)
- Методы:
  - get_serializer_class(self):  
  Определяет, какой сериализатор использовать для ответа.
  Возвращает UserSerializer для администраторов и владельца,
  а UserGeneralSerializer для обычных пользователей.
- Доступ:
  - авторизованному пользователю
### UserUpdateAPIView:
Представление для обновления пользователя по идентификатору (PUT/PATH)
- Доступ:
  - авторизованному пользователю:
    - владелец
### UserDestroyAPIView:
Представление для удаления пользователя по идентификатору (DELETE)
- Доступ:
  - сотрудник
### PaymentListAPIView:
Представление для получения списка всех платежей (GET)
Сортировка: дате(date_pay)
Фильтрация: курсу(course), уроку(lesson), методу платежа(payment_method)
- Доступ:
  - сотрудник

[<- на начало](#содержание)

---