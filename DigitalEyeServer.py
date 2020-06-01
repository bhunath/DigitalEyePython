import base64

import cv2
import numpy as np
from bson.json_util import dumps
from flask import Flask, request
from flask_cors import CORS, cross_origin


from DigitalEyeDAO import store_blink, fetch_blink_report_per_minute, fetch_exposure_data, fetch_closeness_data, \
    store_touch, fetch_touch_data
from DigitalEyeDetectBlink import process_image_for_blink_detection, get_blink_count


app = Flask(__name__)

import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

CORS(app)


@app.route("/uploadImage", methods=['post'])
def upload_image():
    result = {'Blink_Count': 0, 'Blink_Message': ''}
    image_string = request.form['file'].split(",")[1]
    img_data_b_64 = base64.b64decode(image_string)
    img_np_arr = np.fromstring(img_data_b_64, np.uint8)
    image = cv2.imdecode(img_np_arr, cv2.IMREAD_COLOR)
    previous_blink_count = get_blink_count()
    blink_count = process_image_for_blink_detection(image)
    if type(blink_count) == int and blink_count > previous_blink_count:
        result['Blink_Count'] = blink_count
        store_blink(1)
    if type(blink_count) != int:
        result['Blink_Count'] = previous_blink_count
        result['Blink_Message'] = blink_count
    if type(blink_count) == int and blink_count == previous_blink_count:
        result['Blink_Count'] = blink_count
    return dumps(result)


@app.route("/stop_capturing")
def stop_capturing():
    # Close Any Resource if want
    return "Stopped Capturing Blink"


@app.route("/fetch_blink", methods=['post'])
def fetch_blink():
    print('inside fetch_blink_per_minute_data')
    groupBY = request.get_json()['groupBy']
    return fetch_blink_report_per_minute(1, groupBY)


@app.route("/fetch_exposure_data", methods=['post'])
def fetch_exposure_report():
    groupBY = request.get_json()['groupBy']
    return fetch_exposure_data(1, groupBY)


@app.route("/closeness_data", methods=['post'])
def fetch_closeness_report():
    groupBY = request.get_json()['groupBy']
    return fetch_closeness_data(1, groupBY)


@app.route("/touch_data")
def fetch_touch_report():
    groupBY = request.get_json()['groupBy']
    return fetch_touch_data(1, groupBY)


@app.route("/store_face_touch", methods=['post'])
def store_face_touch():
    print(request.get_json())
    return store_touch(request.get_json()['user_id'])


def start_server():
    app.run(debug=False, host='0.0.0.0', port=8080)

