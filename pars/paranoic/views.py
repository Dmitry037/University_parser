from django.http import JsonResponse
from geminiparser import parse_schedule, get_schedule

def my_info_view(request):
    week = 30
    our_url = f'https://ssau.ru/rasp?groupId=1214268581&selectedWeek={week}&selectedWeekday=1'  # здесь будет ссылка
    our_html_content = get_schedule(our_url)
    print(f"HTML content: {our_html_content[:10]}...") #для отладочки
    data = parse_schedule(our_html_content)
    return JsonResponse(data)