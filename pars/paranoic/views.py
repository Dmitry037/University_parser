from django.http import JsonResponse
from gemini_parser import schedule  # Импортируем функцию из вашего скрипта

def my_info_view(request):
    """
    Представление, которое вызывает ваш скрипт и возвращает данные в JSON.
    """
    data = schedule
    return JsonResponse(data)