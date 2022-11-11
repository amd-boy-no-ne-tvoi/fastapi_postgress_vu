FROM python:latest

WORKDIR /code

COPY ./rt.txt /code/rt.txt

RUN pip install --upgrade -r /code/rt.txt

COPY ./app /code/app

CMD [ "uvicorn","app.main:app", "--host", "0.0.0.0", "--port", "8000"]