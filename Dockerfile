# Используем официальный образ Python
FROM python:3.9
# Или другую подходящую версию Python

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /code

# Копируем файлы проекта внутрь контейнера
COPY ./ /code/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Запускаем сервер Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]