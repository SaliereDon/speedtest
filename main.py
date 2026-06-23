import urllib.request as request
import urllib.error
import time
import logging

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

all_requrst_result = []

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f'Функция выполнилась за {end_time - start_time} секунд')
        time.sleep(1) # для пауз между запросами
        if result:
            all_requrst_result.append({'download_time': end_time - start_time})
        return result
    return wrapper


def check_size(func):
     def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result:
            data_size = len(result) * 8
            logger.info(f'Рамер файла: {data_size} Мбит')
            all_requrst_result[-1]['size'] = data_size / 1000000
        return result
     return wrapper

@check_size
@timer
def send_request(url: str) -> dict | None:
    try:
        response = request.urlopen(url, timeout=30)
        data = response.read()
        return data
    except urllib.error.URLError as e:
        logger.error(f'ошибка URL: {e}')
        return None
    except urllib.error.HTTPError as e:
        logger.error(f'Ошибка HTTP: {e}')
        return None
    except Exception as e:
        logger.error(f'Неизвестная ошибка: {e}')
        return None

def avg_speed():
    avg_list = []
    for item in all_requrst_result:
        avg_list.append(item.get('size') / item.get('download_time')) 
    return sum(avg_list) / len(avg_list)

def main():
    i = 0
    while i < 10:
        send_request(url='https://github.com/szalony9szymek/large/releases/download/free/large')
        i += 1
    print(f'Скорость интернета: {avg_speed():.2f} Мбит/с')

if __name__ == '__main__':
    main()