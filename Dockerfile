FROM python:3.9.5

RUN mkdir /app
COPY ./backend/requirements.txt .
RUN pip install -r requirements.txt
COPY . .
WORKDIR /app/backend
CMD gunicorn --chdir /backend foodgram.wsgi:application --bind 0.0.0.0:8000