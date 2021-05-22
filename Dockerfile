FROM python:3.9.5

ADD *.py /CIVBot/
ADD /Bots /CIVBot/Bots
ADD configuration.yml /CIVBot/

WORKDIR /CIVBot

RUN pip install pyyaml python-telegram-bot pymongo

CMD python start.py
