FROM python:3.7-slim

RUN mkdir -p /app
COPY requirements.txt /app
WORKDIR /app
RUN apt-get update -qq && apt-get install -yqq \
    git \
    && rm -rf /var/lib/apt/lists
RUN pip install -r requirements.txt
ADD . /app
ENV WORKERS=2
ENV PORT=8000

EXPOSE $PORT
CMD gunicorn -b :$PORT -w $WORKERS wsgi --log-level info
