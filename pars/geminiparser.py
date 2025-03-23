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
    """
    if not html_content or html_content.startswith("Error"):
        print("Ошибка: HTML-содержимое недоступно или пустое.")
        return {}

    soup = BeautifulSoup(html_content, 'html.parser')
    # Убираем recursive=False для поиска корневого контейнера
    schedule_items_container = soup.find('div', class_='schedule__items')

    # ПРОВЕРКА НА НАЛИЧИЕ КОНТЕЙНЕРА
    if schedule_items_container is None:
        print("Контейнер потерялся")
        return {}  # Возвращаем пустой словарь, если контейнер не найден

    # Извлекаем все элементы schedule__item
    schedule_items = schedule_items_container.find_all('div', class_='schedule__item', recursive=False)

    # Извлекаем дни недели
    weekdays = []
    for item in schedule_items:
        if 'schedule__head' in item.get('class', []):
            weekday_div = item.find('div', class_='schedule__head-weekday')
            if weekday_div:
                weekdays.append(weekday_div.text.strip())

    if not weekdays:
        return {}  # Если нет дней недели, возвращаем пустой словарь

    # Инициализируем промежуточный словарь расписания (по времени)
    schedule_by_time = {}

    # Находим все временные интервалы
    time_divs = schedule_items_container.find_all('div', class_='schedule__time', recursive=False)

    # Если нет временных интервалов, возвращаем пустой словарь
    if not time_divs:
        return {}

    # Обрабатываем каждый временной интервал
    for time_index, time_div in enumerate(time_divs):
        time_items = time_div.find_all('div', class_='schedule__time-item')
        if len(time_items) == 2:
            start_time = time_items[0].text.strip()
            end_time = time_items[1].text.strip()
            time_range = f"{start_time} - {end_time}"
            schedule_by_time[time_range] = []
        else:
            continue  # Пропускаем некорректные временные интервалы

        # Находим занятия, которые следуют сразу после текущего временного интервала
        time_div_index = list(schedule_items_container.children).index(time_div)
        lesson_items = []
        for i in range(time_div_index + 1, len(list(schedule_items_container.children))):
            next_item = list(schedule_items_container.children)[i]
            if isinstance(next_item, str):  # Пропускаем текстовые узлы (пробелы, переносы строк)
                continue
            if next_item.get('class') and 'schedule__time' in next_item.get(
                    'class'):  # Останавливаемся, если встретили следующий schedule__time
                break
            if next_item.get('class') and 'schedule__item' in next_item.get('class'):
                lesson_items.append(next_item)

        # Обрабатываем занятия для каждого дня недели
        for lesson_index, lesson_item in enumerate(lesson_items):
            if lesson_index >= len(weekdays):  # Если занятий больше, чем дней недели, прерываем
                break

            lesson_div = lesson_item.find('div', class_='schedule__lesson')
            if lesson_div:
                lesson_info = {}
                lesson_info['weekday'] = weekdays[lesson_index]
                lesson_info['time'] = time_range  # Добавляем время занятия

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

                schedule_by_time[time_range].append(lesson_info)

    # Перестраиваем расписание по дням недели
    schedule_by_weekday = {}
    for time_range, lessons in schedule_by_time.items():
        for lesson in lessons:
            if lesson:  # Пропускаем пустые занятия ({})
                weekday = lesson['weekday']
                if weekday not in schedule_by_weekday:
                    schedule_by_weekday[weekday] = []

                # Удаляем ненужные поля и добавляем занятие в расписание по дню недели
                filtered_lesson = {
                    'time': lesson['time'],
                    'type': lesson['type'],
                    'discipline': lesson['discipline'],
                    'place': lesson['place']
                }
                schedule_by_weekday[weekday].append(filtered_lesson)

    return schedule_by_weekday

week = 30
our_url = f'https://ssau.ru/rasp?groupId=1214268581&selectedWeek={week}&selectedWeekday=1' #здесь будет ссылка
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