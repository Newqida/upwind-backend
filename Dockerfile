FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

RUN addgroup --system django \
    && adduser --system --ingroup django django

COPY test.sh /
RUN chmod +x /test.sh
RUN chown django /test.sh

COPY --chown=django:django . /app

USER django

WORKDIR /app