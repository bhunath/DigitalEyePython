import numpy as np
from flask import Flask, request

from pymongo import MongoClient
from bson.json_util import dumps
from flask_cors import CORS, cross_origin
import cv2
import base64
from DigitalEyeDetectBlink import process_image_for_blink_detection, get_blink_count
from DigitalEyeDAO import store_blink, fetch_blink_report_per_minute , fetch_exposure_data

client = MongoClient('localhost', 27017)
db = client.digital_eyes
pythonTest = db.eye_blink_stats

app = Flask(__name__)

import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

CORS(app)


@app.route("/fetchBlinkStat")
@cross_origin()
def fetch_blink_stat():
    json = dumps(pythonTest.find())
    return json


@app.route("/uploadImage", methods=['post'])
def upload_image():
    image_string = request.form['file'].split(",")[1]
    img_data_b_64 = base64.b64decode(image_string)
    img_np_arr = np.fromstring(img_data_b_64, np.uint8)
    image = cv2.imdecode(img_np_arr, cv2.IMREAD_COLOR)
    previous_blink_count = get_blink_count()
    blink_count = process_image_for_blink_detection(image)
    if type(blink_count) == int and blink_count > previous_blink_count:
        store_blink(1)
    return "Blink Count {}".format(blink_count)


@app.route("/stop_capturing")
def stop_capturing():
    # Close Any Resource if want
    return "Stopped Capturing Blink"


@app.route("/fetch_blink_per_minute_data")
def fetch_blink_per_minute_report():
    print('inside fetch_blink_per_minute_data')
    return fetch_blink_report_per_minute(1)


@app.route("/fetch_exposure_data")
def fetch_exposure_report():
    return fetch_exposure_data(1)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
