FROM python:3.11.6-bookworm

WORKDIR /code/

COPY requirements.txt /code/

RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . /code/

EXPOSE 8000