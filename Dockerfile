FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /socialnetwork
COPY requirements.txt /socialnetwork/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /socialnetwork/
EXPOSE 8000