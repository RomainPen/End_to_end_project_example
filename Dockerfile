FROM python:3.12-slim

WORKDIR /app/backend

COPY . /app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 80

CMD uvicorn API:api --host 0.0.0.0 --port $PORT

# local testing : $PORT = 80