FROM gliderlabs/alpine:3.3

RUN apk add --update python py-pip
RUN pip install --upgrade pip

ADD ./requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN mkdir /root/.credentials

COPY sheets.googleapis.com-python-smsbot.json /root/.credentials/

RUN mkdir /smsbot

COPY . /smsbot/
