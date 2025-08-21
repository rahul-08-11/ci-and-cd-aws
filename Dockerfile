FROM python:alpine3.21

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

ENTRYPOINT [ "python" ]

CMD [ "main.py" ]