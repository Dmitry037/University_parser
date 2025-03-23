import requests
from bs4 import BeautifulSoup


def get_schedule(url):
    # Получаем HTML-код страницы
    response = requests.get(url)
    response.raise_for_status()  # Проверяем, что запрос успешен (статус 200 OK)
    return response.text


def parse_schedule(html_content):
    """
    Извлекает расписание из HTML-кода и возвращает его в структурированном формате.

    Args:
        html_content: Строка, содержащая HTML-код расписания.

    Returns:
        Словарь, представляющий расписание.  Ключи - временные интервалы (строки).
        Значения - списки словарей (по одному словарю на каждый день недели).
        Каждый словарь содержит информацию о занятии: 'weekday', 'discipline', 'type', 'place', 'teacher', 'groups', 'comment'.
        Если занятий нет, то словарь пустой.
    """

    soup = BeautifulSoup(html_content, 'html.parser')
    schedule_items_container = soup.find('div', class_='schedule__items')
    schedule_items = schedule_items_container.find_all('div', class_='schedule__item',
                                                       recursive=False)  # Только непосредственные дочерние элементы
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
        return {}  # Возвращаем пустой словарь, если дни недели не найдены

    time_index = 0
    lesson_index = len(weekdays)  # Индекс, с которого начинаются занятия

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
                # Обработка некорректного формата времени
                time_index += 1
                continue

        else:
            break  # Выход из цикла если закончились временные интервалы

        # Извлечение занятий для данного временного интервала
        for weekday_index in range(len(weekdays)):
            current_lesson_item = schedule_items[lesson_index + weekday_index]

            if 'schedule__lesson' in [tag.name for tag in current_lesson_item.find_all(recursive=False)]:
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
                        if not groups:  # Handle cases where groups are empty spans
                            for group_span in groups_container.find_all('span', class_='caption-text'):
                                if group_span.text.strip():
                                    groups.append(group_span.text.strip())
                    lesson_info['groups'] = groups

                    comment = lesson_info_div.find('div', class_='schedule__comment')
                    lesson_info['comment'] = comment.text.strip() if comment else ''

                schedule[time_range].append(lesson_info)

            else:
                # Добавление пустого словаря, если занятия нет
                schedule[time_range].append({})

        lesson_index += len(weekdays)
        time_index += 1

    return schedule


our_url = '' #здесь будет ссылка
# пример ссылки https://ssau.ru/rasp?groupId=530996285&selectedWeek=29&selectedWeekday=3
#our_html_content = get_schedule(our_url)





"""
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
"""