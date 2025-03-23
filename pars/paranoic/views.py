from django.http import JsonResponse
from geminiparser import parse_schedule  # мудак Pycharm мне неправильный импорт навязал

def my_info_view(request):
    ### warring only for test!!!!
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
        pass #для отладочки
    our_html_content = read_html_from_file('structure.html')

    ### warring only for test!!!!
    print(f"HTML content: {our_html_content[:10]}...") #для отладочки
    data = parse_schedule(our_html_content)
    return JsonResponse(data)