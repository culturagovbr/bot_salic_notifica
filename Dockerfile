FROM python:3.5

ADD . /srv

WORKDIR /srv
RUN pip install -r requirements.txt

CMD ["python", "/srv/bot.py"]
