# BLACKWALL Тестовое задание

### Описание задания:

Требуется разработать систему транзакций.

Транзакции должны составляться в очередь на выход. Очередь связана с клиентом.

## Важно!
 - Транзакции должны быть атомарными
 - В качестве СУБД должна использоваться PostgreSQL

## Основные фичи проекта

Основное задание реализовано с помощью фичи psycopg2 в Django Framework:

«
```Python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str('POSTGRES_DB'),
        'USER': env.str('POSTGRES_USER'),
        'PASSWORD': env.str('POSTGRES_PASSWORD'),
        'HOST': env.str('POSTGRES_HOST'),
        'PORT': env.int('POSTGRES_PORT'),
        'ATOMIC_REQUESTS': True, # <-- Принудительная атомарность всех транзакций
    }
}
```
»

Данный параметр заставляет все транзакции совершать атомарно. 
У данного подхода есть один нюанс. Он работает **Только с необработанными исключениями**

## Решение проблемы с необработанными исключениями

Чтобы решить проблему с исключениями, которые могут обрушить работу сервера, существует изящное решение,
через **django middleware**

**\BlackWall\transactions\middleware.py**

``` Python
from django.http import JsonResponse
from rest_framework import status


class ProcessException:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        return self._get_response(request)

    def process_exception(self, request, exception):
        return JsonResponse(str(exception), safe=False, status=status.HTTP_402_PAYMENT_REQUIRED)

```

Данный middleware перехватывает метод get_response и ждет exception, но не обрабатывает его, а выводит JsonResponse
c сообщением об ошибке для клиента.

**!!!Особенно важно донести до команды, не использовать try catch при работе с транзакциями!!!**

Так же, некоторые валидаторы сериализаторов имеют под капотом ```raise``` для вызова исключения. Что позволяет обрабатывать
подобные сообщения с помощью middleware

## Описание решения

Решение выбрано одно из самых простых, были переопределены методы create у сериализаторов и методы save у моделей.
Я отказался от использования сигналов, так как в данном проекте не вижу большой необходимости в их использовании.
Как вариант построения системы траназкций, связанных с очередями и клиентами, можно было использовать: 
- Переопледеление метода post/create в Views Django Rest Framework
- Переопределение метода create в сериализаторах
- Написание сигналов к модели ```transaction```


## Описание системы транзакций

### Клиент
Модель клиента связана один-к-одному с моделью User из модуля ```auth``` django
и связана отношением многие-ко-многим с модель ```Queue```

#### Создание клиента:

Создание клиента с помощью пост запроса на url: ``127.0.0.1:8000/api/v1/client/``

```Json
{
    "name": "Lavrentev", // Имя пользователя
    "password": "5ed903dF", // Пароль
    "purse_number": "123456", // Номер кошелька
    "balance": "3500.0000000000", // Баланс
    "queue": [] // Очереди (могут быть blank)
}
```

Ответ:

```Json
{
  "id": 6,
  "name": "Lavrentev",
  "purse_number": "123456",
  "balance": "3500.0000000000",
  "queue": []
}
```

## Создание очереди

Создание очереди транзакций для клиента с помощью пост запроса на url: ``127.0.0.1:8000/api/v1/queue/``

```Json
{
  "client": 6, // id клиента
  "active": true, // Статус очереди 
  "transaction": [] // Транзакции (Может быть blank)
}
```
Ответ:

```Json
{
  "id": 5,
  "active": true,
  "client": 6,
  "transaction": []
}
```

Проверка клиента: 

GET ```127.0.0.1:8000/api/v1/client/6/```

Ответ:

```Json
{
  "id": 6,
  "name": "Lavrentev",
  "purse_number": "123456",
  "balance": "3500.0000000000",
  "queue": [
    5
  ]
}
```

## Создание транзакции

Создание транзакций для клиента с помощью пост запроса на url: ``127.0.0.1:8000/api/v1/transaction/``

```Json
{
  "value": "500.0000000000", // Значение транзакции
  "operations": "ADD", // Типо операции (ADD || DROP)
  "destination": "123456", // Уникальный номер кошелька
  "queue": 5 // id очереди транзакции
}
```
Ответ:

```Json
{
  "id": 12,
  "value": "500.0000000000",
  "date": "2022-05-17T10:29:44.326359Z",
  "operations": "ADD",
  "destination": "123456",
  "queue": 5
}
```

## Проверка операции

Проверка операции пополнения кошелька клиента с помощью GET запроса на ``127.0.0.1:8000/api/v1/client/id/``

Ответ:

```Json
{
  "id": 6,
  "name": "Lavrentev",
  "purse_number": "123456",
  "balance": "4000.0000000000", // <-- состояние изменилось
  "queue": [
    5
  ]
}
```

Проверка очереди:

GET ```127.0.0.1:8000/api/v1/queue/id/```

Ответ:

```Json
{
  "id": 5,
  "active": true,
  "client": 6,
  "transaction": [
    12 // <-- добавилась транзакция
  ]
}
```

## Проверка обработки исключений

Проверка обработки исключений с помощью снятия с кошелька клиента большей суммы, чем имеется у клиента, при помощи пост запроса:

```Json
{
  "value": "11500.0000000000",
  "operations": "DROP",
  "destination": "123456",
  "queue": 5
}
```

Ответ:

```Json
"{'success': False, 'errorMessage': 'Недостаточно средств'}"
```

Проверяем состояние очереди:

GET ```127.0.0.1:8000/api/v1/queue/id/```

```Json
{
  "id": 5,
  "active": true,
  "client": 6,
  "transaction": [
    12 // <-- Транзакция не изменилась
  ]
}
```

Проверяем состояние кошелька:

GET ```127.0.0.1:8000/api/v1/client/id/```

ответ

```Json
{
  "id": 6,
  "name": "Lavrentev",
  "purse_number": "123456",
  "balance": "4000.0000000000", // <-- состояние кошелька не изменилось
  "queue": [
    5
  ]
}
```

# Деплой проекта

## Стек

- Django 3.2
- Django Rest Framework 3.13
- pipenv для вирутального окружения
- postgresql 12.0
- Docker compose

## клонирование проекта:

 - Склонируйте проект с github

 - ```git clone git@github.com:BordKanone/BlackWall.git .```

 - [Установите докер](https://www.docker.com/get-started/)
 - Выполните команду: ```docker-compose up -d --build --remove-orphans```
 - Дождитесь деплоя проекта
 - Выполните запрос на ```127.0.0.1:8000/api/v1/queue/```