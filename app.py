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
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    meetingtype = parameters.get("meetingtype")

    cost = {'mc':'meeting center', 'tc':'training center', 'ec':'event center'}

    speech = zone + " is " + str(cost[zone]) + "."

    print("Response:")
    print(speech)

    return {
        "data" : {
        "basicCard": {
                    "title": "title",
                    "subtitle": "subtitle",
                    "formattedText": "text",
                    "image": {
                        "url": "https://www.webex.com/content/dam/webex/eopi/Americas/USA/en_us/global/images/logos/Cisco_WebEx_wordmark_lockupx2.png"
                    },
                    "buttons": [
                        {
                            "title": "My PMR",
                            "openUrlAction": {
                                "url": "https://www.go.webex.com/meet/yingczha"
                            }
                        }
                    ]
                }
        },
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
