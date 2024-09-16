FROM python:3.12-alpine

COPY . /api
WORKDIR /api

RUN apk upgrade --no-cache

RUN apk add --no-cache --virtual build-deps  py3-pip build-base python3-dev libffi-dev openssl-dev gcc musl-dev
RUN pip install --no-cache --upgrade pip setuptools
RUN apk add --no-cache mariadb-dev

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apk del build-deps
EXPOSE 8080

RUN chmod +x ./start.sh
RUN mkdir /var/log/api/ && touch /var/log/api/gunicorn_error.log && touch /var/log/api/api.log && touch /var/log/api/gunicorn_access.log
RUN chown -R 1001:1001 /var/log/api/
USER 1001:1001
CMD ["./start.sh"]