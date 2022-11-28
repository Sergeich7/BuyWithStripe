FROM python:3.9-slim
LABEL maintainer="Vitaly Belashov pl3@yandex.ru"
WORKDIR /app
RUN pip install --upgrade pip
COPY requirements.txt start.sh /app/
RUN pip install -r requirements.txt
EXPOSE 8000
RUN chmod +x start.sh
ENV PYTHONUNBUFFERED 1
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
