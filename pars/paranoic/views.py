from django.http import JsonResponse
from geminiparser import parse_schedule, get_schedule
from Timer import calculate_weeks_since_start_date

def my_info_view(request):
    week = calculate_weeks_since_start_date()
    our_url = f'https://ssau.ru/rasp?groupId=1214268581&selectedWeek={week}&selectedWeekday=1'  # здесь будет ссылка
    our_html_content = get_schedule(our_url)
    data = parse_schedule(our_html_content)
    return JsonResponse(data)