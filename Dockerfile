FROM python:3.11-alpine

EXPOSE 8001

RUN apk --update add curl

WORKDIR /src

RUN python -m pip install --upgrade pip

COPY /requirements.txt .

RUN python -m pip install -r requirements.txt

COPY src .

CMD [ "sh", "-c", "alembic upgrade head && uvicorn main:app --workers 3 --timeout-keep-alive 300 --host 0.0.0.0 --port 8001" ]
