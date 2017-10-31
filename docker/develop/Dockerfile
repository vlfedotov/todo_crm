FROM python:3.6-alpine

ADD requirements /opt/requirements
RUN pip install -r /opt/requirements/requirements.dev.txt gunicorn

ADD src /opt/app
WORKDIR /opt/app
