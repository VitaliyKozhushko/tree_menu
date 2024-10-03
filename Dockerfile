FROM python:3.10-alpine

RUN apk add --update --no-cache --virtual .tmp-build-deps \
        postgresql-dev gcc musl-dev libpq-dev python3-dev

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
