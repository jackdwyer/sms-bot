#!/usr/bin/env python
from flask import Flask, request, redirect, Response
from functools import wraps
import twilio.twiml
import os
import datetime
import logging
import sheets

TWILIO_USER_AGENT = os.environ['TWILIO_USER_AGENT']
TWILIO_SIGNATURE = os.environ['TWILIO_SIGNATURE']

# headers we care for
# user-agent ==  TwilioProxy/1.1
# X-Twilio-Signature == something base64 ? (6l37Br/FUmpHMK6rVjBGvK3CPgo=)

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.DEBUG)
app.logger.disabled = False

app.count = 0

# handler = logging.StreamHandler()
# handler.setLevel(logging.DEBUG)
# app.logger.addHandler(handler)

gclient = sheets.Gsheet(os.environ['SPREADSHEET_ID'], os.environ['SPREADSHEET_CONFIG'])


def requires_headers(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.headers.get('user-agent', None) == 'TwilioProxy/1.1':
            return Response('Failure')
        if not request.headers.get('x-twilio-signature', None) == '':
            pass
        return f(*args, **kwargs)
    return decorated


def sms_help():
    _str = "Usage:\n"
    for key, val in gclient.config.items():
        _str += "{0} {1}\n".format(key, val)
    return _str


def parse_message(msg):
    msg = msg.lower()
    print("entered parse message")
    print(msg)
    if msg in ["?", "help"]:
        return sms_help()
        # _str = "Usage:\n"
        # for key, val in gclient.config.items():
        #     _str += "{0} {1}\n".format(key, val)
        # response = _str
    elif msg == "Beer" or msg == "beer" or msg == "BEER" or msg == "c":
        print("in here")
        app.count += 1
        response = "Current count: {}".format(str(app.count))
    else:
        d = str(msg)
        print(d)
        data = d.split(' ', 1)
        print('actual data')
        print(data)
        try:
            print('printing gclient')
            print(gclient.config[data[0]])
        except KeyError:
            print("KEY ERROR line 69")
            print(data[0])
            return 'errored the fuck out'
        if gclient.append_value([str(datetime.datetime.now()), data[1]], data[0]):
            response = "Value appended to: {}".format(gclient.config[data[0]])
        else:
            return sms_help()
    return response


@app.route("/", methods=['POST'])
@requires_headers
def index():
    _num_segments = request.form['NumSegments']
    _from = request.form['From']
    _body = request.form['Body']

    app.logger.info("from: {} | segments: {} | body: {}".format(_from, _num_segments, _body))

    outcome = parse_message(_body)

    resp = twilio.twiml.Response()
    resp.message(outcome)
    return str(resp)


@app.route("/health")
def health():
    return 'ok'


if __name__ == "__main__":
    app.logger.info("======================== NEW RELEASE =========================\n")
    app.run(host='0.0.0.0')
