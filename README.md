# GLADOS
Сервис аккаунтов и входа для платформы Slotty.

## Стек
* Python 3.12
* FastAPI
* Uvicorn
* Docker

## Быстрый запуск (через Docker)
Для запуска сервиса выполните команду:
```bash
sudo docker compose up --build

Сервис будет доступен по адресу: http://localhost:8000

## Проверка работоспособности
Отправьте GET-запрос на эндпоинт /status:
curl http://localhost:8000/status

Ожидаемый ответ: {"status": "OK"}

## Остановка сервиса
Нажмите Ctrl + C в терминале или выполните:
sudo docker compose down
