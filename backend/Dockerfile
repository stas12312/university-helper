FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/src
WORKDIR /src


RUN pip install pipenv
COPY Pipfile Pipfile.lock /src/
RUN pipenv install --system --dev

COPY ./src /src

