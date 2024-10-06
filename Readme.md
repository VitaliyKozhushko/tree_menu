# Тестовое задание

Оторазить на странице древовидное меню

## Содержание
1. [Требования](#main_requirements)
2. [Стек технологий](#technology_stack)
3. [Инструкция по запуску проекта](#instruction_startup)
4. [Особенности](#features)
5. [Тестирование](#testing)

## Требования <a name="main_requirements"></a>

Задача :
Нужно сделать django app, который будет реализовывать древовидное меню, соблюдая следующие условия:
1) Меню реализовано через template tag
2) Все, что над выделенным пунктом - развернуто. Первый уровень вложенности под выделенным пунктом тоже развернут.
3) Хранится в БД.
4) Редактируется в стандартной админке Django
5) Активный пункт меню определяется исходя из URL текущей страницы 
6) Меню на одной странице может быть несколько. Они определяются по названию.
7) При клике на меню происходит переход по заданному в нем URL. URL может быть задан как явным образом, так и через named url.
8) На отрисовку каждого меню требуется ровно 1 запрос к БД
Нужен django-app, который позволяет вносить в БД меню (одно или несколько) через админку, и нарисовать на любой нужной странице меню по названию.
{% draw_menu 'main_menu' %}
При выполнении задания из библиотек следует использовать только Django и стандартную библиотеку Python.

## Стэк технологий <a name="technology_stack"></a>

- Backend: [Django](https://www.djangoproject.com/)
- Database: [PostgreSQL](https://www.postgresql.org/)

## Инструкция по запуску проекта <a name="instruction_startup"></a>

1. Клонируйте репозиторий
```
git clone https://github.com/VitaliyKozhushko/tree_menu.git
```
2. Настройте .env файл
3. Запустите проект:
   * (суперпользователь будет автоматически создан - login: admin, password - admin)
   - либо в ручном режиме (предварительно активировав среду venv):
      ```shell
        pip install -r requirements.txt
        python manage.py collectstatic
        python manage.py makemigrations
        python manage.py migrate
        python create_superuser.py
        python manage.py runserver
        ```
   - либо с помощью docker
   ```shell
   docker compose up --build
   ```
   
## Особенности <a name="features"></a>

- на главной странице отображаются меню только с url либо с named url
- переход на страницу меню при клике на название меню
- обработка named_url добавленных в urls.py
- если нет шаблона для named_url в urls.py, то будет автоматически передресовано на осн. шаблон
- при указании одновременно url и named url, за основу будет взят url

## Требования <a name="testing"></a>

Для запуска тестов выполнить команду
```shell
   python manage.py test
```