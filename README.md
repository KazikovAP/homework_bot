[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
![API](https://img.shields.io/badge/API-orange)

# Homework Bot

---
## Описание проекта
Homework Bot - телеграм-бот для проверки статуса домашней работы через API-сервис Практикум.Домашка. 

---
## Функционал бота
- Раз в 10 минут опрашивает API сервис Практикум.Домашка и проверет статус отправленной на ревью домашней работы;
- При обновлении статуса анализирует ответ API и отправляет соответствующее уведомление в Telegram;
- Логирует свою работу и сообщает о важных проблемах сообщением в Telegram.

---
## Технологии
* Python 3.9
* API

---
## Запуск бота

Для MacOs и Linux вместо python использовать python3

**1. Клонировать репозиторий:**
```
git clone https://github.com/KazikovAP/homework_bot.git
```

**2. Перейти в папку проекта:**
```
cd /homework_bot/
```

**3. Cоздать и активировать виртуальное окружение:**
```
python -m venv venv
```

Для Windows:
```
source venv/Scripts/activate
```

Для MacOs/Linux:
```
source venv/bin/activate
```

**4. Установить зависимости из файла requirements.txt:**
- Обновить пакетный менеджер pip
```
python -m pip install --upgrade pip
```

- Установить зависимости
```
pip install -r requirements.txt
```

**5. Создать файл .env для хранения ключей:**
```
PRACTICUM_TOKEN=<PRACTICUM_TOKEN> # Токен профиля на Яндекс.Практикуме
TELEGRAM_TOKEN=<TELEGRAM_TOKEN> # Tокен профиля на Яндекс.Практикуме
CHAT_ID=<CHAT_ID> # Cвой ID в телеграме
```

**6. Запустить бота:**
```
python homework.py
```

---
## Разработал:
[Aleksey Kazikov](https://github.com/KazikovAP)

---
## Лицензия:
[MIT](https://opensource.org/licenses/MIT)
