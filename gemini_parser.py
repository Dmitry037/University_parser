import requests
from bs4 import BeautifulSoup

def get_schedule(url):
    """
    Извлекает расписание с веб-страницы.

    Args:
        url: URL страницы с расписанием.

    Returns:
        Список словарей, представляющих собой расписание,
        или None, если произошла ошибка.
    """
    try:
        # 1. Получаем HTML-код страницы
        response = requests.get(url)
        response.raise_for_status()  # Проверяем, что запрос успешен (статус 200 OK)

        # 2. Создаем объект BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(response.text, 'lxml')  # Используем lxml как парсер

        # 3. Ищем элементы с расписанием (пример для гипотетической структуры)
        schedule_items = soup.find_all('div', class_='schedule-item')  # Ищем все div с классом schedule-item

        schedule = []
        for item in schedule_items:
            # 4. Извлекаем данные из каждого элемента
            try:
                # Предположим, что структура такая:
                # <div class="schedule-item">
                #   <span class="time">10:00</span>
                #   <span class="title">Лекция по математике</span>
                #   <span class="location">Аудитория 101</span>
                # </div>

                time = item.find('span', class_='time').text.strip()
                title = item.find('span', class_='title').text.strip()
                location = item.find('span', class_='location').text.strip()

                schedule.append({
                    'time': time,
                    'title': title,
                    'location': location,
                })
            except AttributeError:
                # Обработка случая, когда одного из элементов нет
                print(f"Ошибка при обработке элемента: {item}")
                continue  # Переходим к следующему элементу

        return schedule

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к сайту: {e}")
        return None
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        return None


# Пример использования
url = "https://example.com/schedule"  # Замените на URL страницы с вашим расписанием
schedule = get_schedule(url)

if schedule:
    for item in schedule:
        print(f"Время: {item['time']}, Предмет: {item['title']}, Аудитория: {item['location']}")
else:
    print("Не удалось получить расписание.")