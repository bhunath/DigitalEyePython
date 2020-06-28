import base64

import cv2
import numpy as np
from bson.json_util import dumps
from flask import Flask, request
from flask_cors import CORS, cross_origin
from threading import Thread

from DigitalEyeDAO import store_blink, fetch_blink_report_per_minute, fetch_exposure_data, fetch_closeness_data, \
    store_touch, fetch_touch_data, store_user_settings, fetch_user_settings
from DigitalEyeDetectBlink import process_image_for_blink_detection, get_blink_count
from DigitalEyeUtils import DigitalEyeUtils

app = Flask(__name__)

import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
utils = DigitalEyeUtils()

CORS(app)


@app.route("/uploadImage", methods=['post'])
def upload_image():
    result = {'Blink_Count': 0, 'Blink_Message': ''}
    image_string = request.form['file'].split(",")[1]
    img_data_b_64 = base64.b64decode(image_string)
    img_np_arr = np.fromstring(img_data_b_64, np.uint8)
    image = cv2.imdecode(img_np_arr, cv2.IMREAD_COLOR)
    previous_blink_count = get_blink_count()
    captureCloseness = True if request.form['closeness'] == 'true' else False
    captureRedness = True if request.form['redness'] == 'true' else False
    blink_count = process_image_for_blink_detection(image, captureCloseness, captureRedness)
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

@app.route("/fetch_settings", methods=['get'])
def fetch_settings():
    print('inside fetch_settings')
    settings = fetch_user_settings(1)
    if settings is not None :
        return settings
    return {}

@app.route("/try_long_break", methods=['get'])
def route_try_long_break():
    print('inside try_long_break')
    return utils.try_long_break()

@app.route("/try_short_break", methods=['get'])
def route_try_short_break():
    print('inside try_short_break')
    return utils.try_short_break()

@app.route("/try_blink_notification", methods=['get'])
def route_try_blink_notification():
    print('inside try_blink_notification')
    return utils.try_blink_notification()


@app.route("/fetch_exposure_data", methods=['post'])
def fetch_exposure_report():
    groupBY = request.get_json()['groupBy']
    return fetch_exposure_data(1, groupBY)


@app.route("/closeness_data", methods=['post'])
def fetch_closeness_report():
    groupBY = request.get_json()['groupBy']
    return fetch_closeness_data(1, groupBY)


@app.route("/touch_data", methods=['post'])
def fetch_touch_report():
    groupBY = request.get_json()['groupBy']
    return fetch_touch_data(1, groupBY)


@app.route("/store_face_touch", methods=['post'])
def store_face_touch():
    print(request.get_json())
    return store_touch(request.get_json()['user_id'])


@app.route("/store_settings", methods=['post'])
def store_settings():
    print(request.get_json())
    saved_settings = store_user_settings(1,request.get_json())
    return saved_settings




def start_server():
    settings = fetch_user_settings(1)
    if settings is not None:
        utils.user_settings_updated(settings)
    app.run(debug=False, host='0.0.0.0', port=8080)
