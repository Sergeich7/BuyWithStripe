FROM python:3.9-slim
LABEL maintainer="Vitaly Belashov pl3@yandex.ru"
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
EXPOSE 8000
COPY . .
ENV PYTHONUNBUFFERED 1
CMD ["./start.sh"]
