FROM python:3.10-slim-bullseye

ENV GUNICORN_WORKERS=2

WORKDIR /opt/milkrage

RUN groupadd milkrage
RUN useradd -g milkrage -M -s /bin/false milkrage

COPY ./requirements.txt ./requirements.txt
COPY ./alembic.ini ./alembic.ini
COPY ./Makefile ./Makefile

RUN pip install --no-cache-dir -r requirements.txt

COPY ./milkrage/ ./milkrage/

USER milkrage

CMD gunicorn 'milkrage:create_app' \
    --workers $GUNICORN_WORKERS \
    --bind 0.0.0.0:5001 \
    --worker-class uvicorn.workers.UvicornWorker
