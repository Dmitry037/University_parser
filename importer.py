# Очень упрощенный пример создания события (без обработки ошибок и аутентификации)

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Загрузка токенов (предполагается, что аутентификация уже пройдена)
creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/calendar'])

# Создание сервиса
service = build('calendar', 'v3', credentials=creds)

# Создание события
event = {
  'summary': 'Тестовое событие',
  'location': 'Онлайн',
  'description': 'Описание тестового события',
  'start': {
    'dateTime': '2024-03-16T10:00:00+03:00',  # Время в формате RFC3339
    'timeZone': 'Europe/Moscow',
  },
  'end': {
    'dateTime': '2024-03-16T11:00:00+03:00',
    'timeZone': 'Europe/Moscow',
  },
  'recurrence': [
    # 'RRULE:FREQ=WEEKLY;UNTIL=20240430T170000Z' # Пример правила повторения
  ],
  'attendees': [
    # {'email': 'testuser@example.com'},  # Пример добавления участника
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'popup', 'minutes': 10},  # Напоминание за 10 минут
    ],
  },
}

# Вставка события в календарь
event = service.events().insert(calendarId='primary', body=event).execute()
print(f"Событие создано: {event.get('htmlLink')}")
