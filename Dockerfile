FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN pip install pipenv
RUN pip install uwsgi
COPY . /app
RUN pipenv install --system
CMD ["/app/start.sh", "--run"]