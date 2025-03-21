import requests
from bs4 import BeautifulSoup


def get_schedule(url):
    # Получаем HTML-код страницы
    response = requests.get(url)
    response.raise_for_status()  # Проверяем, что запрос успешен (статус 200 OK)
    return response.text


def parse_schedule(html_content):
    """
    Извлекает расписание занятий из HTML-структуры.

    Args:
        html_content: HTML-код страницы с расписанием.

    Returns:
        Словарь, где ключи - время, а значения - список словарей с информацией о занятиях
        в это время по дням недели.  Если в какой-то день занятий нет,
        то в списке для этого дня будет пустой словарь {}.
        Пример:
        {
            '08:00 - 09:35': [
                {'weekday': 'понедельник', 'date': '17.03.2025', 'discipline': 'Военная кафедра', 'type': 'Практика', 'place': 'Военная кафедра - 4', 'teacher': 'Преподаватели Военной Кафедры', 'groups': ['2505-240502D', '2507-240502D', '2508-240502D']},
                {}, # Вторник - нет занятий
                {'weekday': 'среда', 'date': '19.03.2025', 'discipline': '...', 'type': '...', ...},
                ...
            ],
            '09:45 - 11:20': [ ... ],
            ...
        }
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    schedule_div = soup.find('div', class_='schedule')
    schedule_items = schedule_div.find_all('div', class_='schedule__item')

    # 1. Извлекаем заголовки (дни недели и даты)
    weekdays = []
    dates = []
    for item in schedule_items:
        if 'schedule__head' in item.get('class', []):
            weekday_div = item.find('div', class_='schedule__head-weekday')
            date_div = item.find('div', class_='schedule__head-date')
            if weekday_div:
                weekdays.append(weekday_div.text.strip())
            if date_div:
                dates.append(date_div.text.strip())

    # 2. Извлекаем время
    times = []
    time_divs = schedule_div.find_all('div', class_='schedule__time')
    for time_div in time_divs:
        time_items = time_div.find_all('div', class_='schedule__time-item')
        for time_item in time_items:
            times.append(time_item.text.strip())

    # 3. Извлекаем информацию о занятиях и группируем по времени
    schedule = {}
    time_index = 0
    day_index = 0

    for item in schedule_items:
        if 'schedule__time' in item.get('class', []):
            # Переход к следующему временному блоку

            continue

        if 'schedule__lesson' in item.findChildren(recursive=False)[0].get('class', []):
            lesson_info = {}

            lesson_type_div = item.find('div', class_='schedule__lesson-type-chip')
            lesson_info['type'] = lesson_type_div.text.strip() if lesson_type_div else ''

            discipline_div = item.find('div', class_='schedule__discipline')
            lesson_info['discipline'] = discipline_div.text.strip() if discipline_div else ''

            place_div = item.find('div', class_='schedule__place')
            lesson_info['place'] = place_div.text.strip() if place_div else ''

            teacher_div = item.find('div', class_='schedule__teacher')
            lesson_info['teacher'] = teacher_div.text.strip() if teacher_div else ''

            groups_div = item.find('div', class_='schedule__groups')
            groups = []
            if groups_div:
                for link in groups_div.find_all('a', class_='schedule__group'):
                    groups.append(link.text.strip())
                lesson_info['groups'] = groups
            else:
                lesson_info['groups'] = []
            if weekdays:
                lesson_info['weekday'] = weekdays[day_index % len(weekdays)]
            if dates:
                lesson_info['date'] = dates[day_index % len(weekdays)]
            if times[time_index] not in schedule:
                schedule[times[time_index]] = []

            schedule[times[time_index]].append(lesson_info)
            day_index += 1

        elif not item.findChildren(recursive=False)[0].get('class') or item.findChildren(recursive=False)[0].get(
                'class') == ['schedule__item_show']:
            # Пустой элемент - нет занятий в этот день для данного времени
            if times[time_index] not in schedule:
                schedule[times[time_index]] = []

            schedule[times[time_index]].append({})  # Добавляем пустой словарь
            day_index += 1
        if day_index > 0 and day_index % len(weekdays) == 0:
            time_index += 1
            if time_index >= len(times):
                break
            day_index = 0

    # 4. Объединяем начальное и конечное время в один слот.
    combined_schedule = {}
    for i in range(0, len(times), 2):
        start_time = times[i]
        end_time = times[i + 1] if i + 1 < len(times) else ""
        combined_time = f"{start_time} - {end_time}"
        # Используем данные из первого найденного
        combined_schedule[combined_time] = schedule.get(start_time, [])

    return combined_schedule


our_url = ''

our_html_content = get_schedule(our_url)
schedule = parse_schedule(our_html_content)


for time_slot, lessons in schedule.items():
    print(f"Время: {time_slot}")
    for lesson in lessons:
        if lesson:  # Проверяем, есть ли информация о занятии
            print(f"  День недели: {lesson.get('weekday', '')}, Дата: {lesson.get('date', '')}")
            print(f"    Дисциплина: {lesson.get('discipline', '')}")
            print(f"    Тип: {lesson.get('type', '')}")
            print(f"    Место: {lesson.get('place', '')}")
            print(f"    Преподаватель: {lesson.get('teacher', '')}")
            print(f"    Группы: {', '.join(lesson.get('groups', []))}")