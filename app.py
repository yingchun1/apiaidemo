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
  "items": [
    {
      "simpleResponse": {
          "textToSpeech": "test basis card",
          #"ssml": string,
          "displayText":  "test basis card"
      }
    },
    {
    "basic_card": {
            "title": "Nearest meeting title",
            "subtitle": "sub title",
            "formatted_text": "text",
            "image": {
                "url": "https://go.webex.com/mw3200/mywebex/html/img/cisco-webex-meetings.png?ver=2452670390"
            },
            "buttons": [
                {
                    "title": "yingczha's personal room",
                    "open_url_action": {
                        "url": "https://go.webex.com/meet/yingczha"
                    }
                }
            ]
        }
    }
  ]
}


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
