from django.http import JsonResponse
from geminiparser import parse_schedule, get_schedule
from Timer import calculate_weeks_since_start_date
from django.core.cache import cache

def my_info_view(request):
    week = calculate_weeks_since_start_date()
    cache_key = f'schedule_data_week_{week}'  # Ключ для кэша, уникальный для каждой недели
    cached_data = cache.get(cache_key)
    if cached_data:
        # Данные найдены в кэше, возвращаем их
        print("Данные взяты из кэша")  # Для отладки
        return JsonResponse(cached_data)
    else:
        # Данных в кэше нет, получаем и парсим расписание
        print("Данные не найдены в кэше, парсим заново")  # Для отладки
        our_url = f'https://ssau.ru/rasp?groupId=1214268581&selectedWeek={week}&selectedWeekday=1'
        our_html_content = get_schedule(our_url)
        data = parse_schedule(our_html_content)

        # Сохраняем данные в кэш на определенное время (например, на 4 часа = 4 * 3600 секунд)
        cache_timeout = 1 * 3600  # Время жизни кэша в секундах (4 часа)
        cache.set(cache_key, data, timeout=cache_timeout)

        return JsonResponse(data)