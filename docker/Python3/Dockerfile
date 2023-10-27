FROM python:3.11.2

WORKDIR /root
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /root/slackbot_aws
COPY ./slackbot_aws ./

ENTRYPOINT /usr/local/bin/python
CMD: ["slackbot.py"]

