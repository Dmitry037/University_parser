from django.http import JsonResponse
from .your_script import get_my_info  # Импортируем функцию из вашего скрипта

def my_info_view(request):
    """
    Представление, которое вызывает ваш скрипт и возвращает данные в JSON.
    """
    data = get_my_info()
    return JsonResponse(data)