FROM python:buster

RUN mkdir /app \
    && pip install 'git+https://github.com/wekan/wekan-python-api-client.git#egg=wekanapi&subdirectory=src' \
    && pip install vobject

COPY wekan_ical_server.py /app/wekan_ical_server.py

CMD [ "python", "/app/wekan_ical_server.py" ]
