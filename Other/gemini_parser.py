import requests
from bs4 import BeautifulSoup
import os
print(os.path.abspath("1.html"))

def get_schedule(url):
    # Получаем HTML-код страницы
    response = requests.get(url)
    response.raise_for_status()  # Проверяем, что запрос успешен (статус 200 OK)
    return response.text


def parse_schedule(html_content):
    """
    Извлекает расписание из HTML-кода и возвращает его в структурированном формате.
    """

    soup = BeautifulSoup(html_content, 'html.parser')
    schedule_items_container = soup.find('div', class_='schedule__items')

    # ПРОВЕРКА НА НАЛИЧИЕ КОНТЕЙНЕРА
    if schedule_items_container is None:
        return {}  # Возвращаем пустой словарь, если контейнер не найден

    schedule_items = schedule_items_container.find_all('div', class_='schedule__item', recursive=False)
    schedule_time_divs = schedule_items_container.find_all('div', class_='schedule__time')

    weekdays = []
    schedule = {}

    # Извлечение дней недели
    for item in schedule_items:
        if 'schedule__head' in item.get('class', []):
            weekday_div = item.find('div', class_='schedule__head-weekday')
            if weekday_div:
                weekdays.append(weekday_div.text.strip())

    # Проверка на пустой список weekdays
    if not weekdays:
        return {}

    time_index = 0
    lesson_index = len(weekdays)

    while lesson_index < len(schedule_items):
        # Извлечение временного интервала
        if time_index < len(schedule_time_divs):
            time_items = schedule_time_divs[time_index].find_all('div', class_='schedule__time-item')
            if len(time_items) == 2:
                start_time = time_items[0].text.strip()
                end_time = time_items[1].text.strip()
                time_range = f"{start_time} - {end_time}"
                schedule[time_range] = []
            else:
                time_index += 1
                continue
        else:
            break

        # Извлечение занятий
        for weekday_index in range(len(weekdays)):
            current_lesson_item = schedule_items[lesson_index + weekday_index]

            # ИСПРАВЛЕННАЯ ПРОВЕРКА НАЛИЧИЯ schedule__lesson
            if any('schedule__lesson' in tag.get('class', []) for tag in current_lesson_item.find_all(recursive=False)):
                lesson_div = current_lesson_item.find('div', class_='schedule__lesson')
                lesson_info = {}
                lesson_info['weekday'] = weekdays[weekday_index]

                # Извлечение типа занятия
                lesson_type_chip = lesson_div.find('div', class_='schedule__lesson-type-chip')
                lesson_info['type'] = lesson_type_chip.text.strip() if lesson_type_chip else ''

                # Извлечение информации о занятии
                lesson_info_div = lesson_div.find('div', class_='schedule__lesson-info')
                if lesson_info_div:
                    discipline = lesson_info_div.find('div', class_='schedule__discipline')
                    lesson_info['discipline'] = discipline.text.strip() if discipline else ''

                    place = lesson_info_div.find('div', class_='schedule__place')
                    lesson_info['place'] = place.text.strip() if place else ''

                    teacher = lesson_info_div.find('div', class_='schedule__teacher')
                    lesson_info['teacher'] = teacher.text.strip() if teacher else ''

                    groups_container = lesson_info_div.find('div', class_='schedule__groups')
                    groups = []
                    if groups_container:
                        for group_link in groups_container.find_all('a', class_='schedule__group'):
                            groups.append(group_link.text.strip())
                        if not groups:
                            for group_span in groups_container.find_all('span', class_='caption-text'):
                                if group_span.text.strip():
                                    groups.append(group_span.text.strip())
                    lesson_info['groups'] = groups

                    comment = lesson_info_div.find('div', class_='schedule__comment')
                    lesson_info['comment'] = comment.text.strip() if comment else ''

                schedule[time_range].append(lesson_info)
            else:
                schedule[time_range].append({})

        lesson_index += len(weekdays)
        time_index += 1

    return schedule


our_url = ''  # Замените на реальный URL, если нужно

# our_html_content = get_schedule(our_url)  # Раскомментируйте, если будете использовать get_schedule

def read_html_from_file(filepath):
    """Читает HTML-содержимое из файла."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:  # Указываем кодировку!
            html_content = f.read()
        return html_content
    except FileNotFoundError:
        return "Error: File not found."
    except Exception as e:
        return f"Error: An error occurred: {e}"


our_html_content = read_html_from_file('1.html')  # Укажите правильный путь к вашему файлу
schedule = parse_schedule(our_html_content)
print(schedule)