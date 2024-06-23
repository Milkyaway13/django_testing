# Описание

В этом проекте написаны тесты для двух Django проектов (для сервиса с заметками пользователей и для новостного сайта). Тесты реализованы с использованием Unittest и Pytest


# Описание
- Python 3.9
- Django
- Pytest
- Unittest

# Установка и запуск

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com//django_testing
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Для Linux/macOS

    ```
    source venv/bin/activate
    ```

* Для Windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
Для запуска тестов unittest перейти в директорию с тестами:
```
cd yanote/notes/tests
```
Запустить все тесты:
```
python -m unittest
```

Для запуска тестов pytest перейти в директорию с тестами:
```
cd ya_news
```
Запустить все тесты:
```
pytest
```

## Автор
[Боярчук Василий](https://github.com/Milkyaway13/)


