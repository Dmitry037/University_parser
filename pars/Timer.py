import datetime


def calculate_weeks_since_start_date():
    """Вычисляет количество полных недель, прошедших с даты начала."""
    start_date = datetime.date(2025, 3, 23)  # даты начала
    today = datetime.date.today()
    delta = today - start_date
    return (delta.days // 7)+30 # Целочисленное деление, чтобы получить полные недели











