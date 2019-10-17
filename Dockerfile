FROM python:buster

COPY wekan_ical_server.py /app

RUN pip install 'git+https://github.com/wekan/wekan-python-api-client.git#egg=wekanapi&subdirectory=src'

CMD [ "python", "wekan_ical_server.py" ]
