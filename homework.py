import time
import os
import logging
import requests
import exceptions
import sys
import json

from http import HTTPStatus
import telegram
from settings import RETRY_PERIOD

from dotenv import load_dotenv

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens() -> bool:
    """Проверяет доступность токенов в окружении."""
    return all((PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID))


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    try:
        logging.info('Начало отправки сообщения')
        bot.send_message(TELEGRAM_CHAT_ID, message)
    except telegram.TelegramError as error:
        error_message = f'Ошибка при отправке сообщения в чат: {error}!'
        logging.error(error_message)
        raise exceptions.SendMessageError(error_message)
    else:
        logging.debug(f'Сообщение успешно отправлено в чат: {message}')


def get_api_answer(timestamp):
    """Делает запрос к эндпоинту API-сервиса."""
    params = {'from_date': timestamp}
    try:
        response = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params=params)
    except requests.exceptions.RequestException as error:
        error_message = f'Ошибка при запросе к API: {error}'
        logging.error(error_message)
        raise exceptions.WrongHttpStatus(error_message)
    status_code = response.status_code
    if status_code != HTTPStatus.OK:
        error_message = (
            f'{ENDPOINT} - недоступен. Код ответа API: {status_code}')
        logging.error(error_message)
        raise exceptions.WrongHttpStatus(error_message)
    try:
        response = response.json()
    except json.JSONDecodeError as error:
        json_error_message = (
            f'данные не являются допустимым форматом JSON: {error}')
        logging.error(json_error_message)
    return response


def check_response(response):
    """Проверяет ответ API на соответствие документации."""
    if not isinstance(response, dict):
        raise TypeError(f'Ответ сервиса не типа - словарь: {response}')
    homeworks = response.get('homeworks')
    if 'homeworks' not in response:
        raise KeyError('Ошибка ключа: нет "homeworks"!')
    if not isinstance(homeworks, list):
        raise TypeError('Ответ сервиса по ключу homeworks не список!')
    return homeworks


def parse_status(homework):
    """Извлекает статус проверки домашней работы."""
    if 'homework_name' not in homework:
        raise KeyError('В ответе API отсутствует ключ "homework_name"!')
    if 'status' not in homework:
        raise KeyError('В ответе API отсутствует ключ "status"!')
    homework_name = homework['homework_name']
    homework_status = homework['status']
    if homework_status not in HOMEWORK_VERDICTS:
        error_message = ('Неизвестный статус домашней работы в ответе API')
        logging.error(error_message)
        raise exceptions.UnknownHomeworkStatus(error_message)
    verdict = HOMEWORK_VERDICTS[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        error_message = 'Отсутствуют переменные окружения!'
        logging.critical(error_message)
        sys.exit('Отсутствуют переменные окружения!')
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    prev_verdict = ''
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            current_timestamp = response.get('current_date', int(time.time()))
            if homeworks:
                verdict = parse_status(homeworks[0])
                send_message(bot, verdict)
                prev_verdict = verdict
                logging.info('Статус получен')
            else:
                status_message = 'Пока не проверили:(\nЖдём дальше...'
                logging.debug(status_message)
                send_message(bot, status_message)
                prev_verdict = status_message
                logging.info(status_message)
        except Exception as error:
            error_message = f'Сбой в работе бота: {error}'
            logging.error(error_message)
            if error_message != prev_verdict:
                send_message(bot, error_message)
                prev_verdict = error_message
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        filename='homework.log',
        format='%(asctime)s: %(levelname)s: %(message)s: %(name)s',
        filemode='w',
        encoding='UTF-8')
    main()
