FROM python:3.9-slim
LABEL maintainer="Vitaly Belashov pl3@yandex.ru"
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 8000
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]