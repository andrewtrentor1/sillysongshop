FROM python:3.13.1-slim-bookworm

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential netcat-traditional \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # Additional dependencies
  && apt-get install -y git \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN addgroup --system django \
    && adduser --system --ingroup django django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./compose/prod/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint
RUN chown django /entrypoint

COPY ./compose/prod/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
RUN chown django /start

COPY ./compose/prod/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker
RUN chown django /start-celeryworker

COPY ./compose/prod/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat
RUN chown django /start-celerybeat

COPY ./compose/prod/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

RUN mkdir /app
RUN mkdir /app/staticfiles
RUN mkdir /app/mediafiles
RUN mkdir /app/logs
RUN chown -R django:django /app
RUN chmod -R 755 /app
RUN chmod -R 775 /app/mediafiles
RUN chmod -R 775 /app/logs
WORKDIR /app

# copy project code
COPY . .

RUN chown -R django:django /app

USER django

ENTRYPOINT ["/entrypoint"]
