#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "meeting.more":
        return {req.get("result").get("action")}
    result = req.get("result")
    parameters = result.get("parameters")
    meetingtype = parameters.get("meetingType")

    cost = {'mc':'meeting center', 'tc':'training center', 'ec':'event center'}

    speech = meetingtype + " is " + str(cost[meetingtype]) + "."

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        "data": {
                            "basicCard": {
                                "title": "Math & prime numbers",
                                "formattedText": "42 is an even composite number. It \n      is composed of three distinct prime numbers multiplied together. It \n      has a total of eight divisors. 42 is an abundant number, because the \n      sum of its proper divisors 54 is greater than itself. To count from \n      1 to 42 would take you about twenty-one…",
                                "image": {
                                    "url": "https://www.google.com/search?q=42",
                                    "accessibilityText": "Image alternate text"
                                },
                                "buttons": []
                            }
                        },
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
