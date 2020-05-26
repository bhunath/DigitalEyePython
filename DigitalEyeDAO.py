import os
from datetime import datetime
from bson.json_util import dumps
from tinydb import TinyDB, Query
import json

dirname = os.getcwd()
db_blink_store = TinyDB(dirname + '/blink_db.json')
db_closeness_store = TinyDB(dirname + '/closeness_db.json')
db_touch_store = TinyDB(dirname + '/touch_db.json')
blink_store_db = db_blink_store.table('blink_store')
closeness_store_db = db_closeness_store.table('closeness_store')
touch_store_db = db_touch_store.table('touch_store')


def store_blink(user_id):
    try:
        inserted_record = blink_store_db.insert({'user_id': user_id, 'blink_time': datetime.today().__str__()})
        print(inserted_record)
        return inserted_record
    except:
        print("Error Occurred while storing blink Record")


def store_touch(user_id):
    try:
        inserted_record = touch_store_db.insert({'user_id': user_id, 'touch_time': datetime.today().__str__()})
        print(inserted_record)
        return "inserted_record"
    except:
        print("Error Occurred in Storing Touch")


def store_closeness(user_id):
    try:
        closeness_record = closeness_store_db.insert({'user_id': user_id, 'close_time': datetime.today().__str__()})
        print('Eye is Close Record', closeness_record)
        return "closeness_record"
    except:
        print("Error Occurred while storing closeness Record")


def fetch_blink_report_per_minute(user_id):
    User = Query()
    blink_records = blink_store_db.search(User.user_id == user_id)
    blink_record_group_by_minute = {};
    for blink_record in blink_records:
        blink_time = datetime.strptime(blink_record.get('blink_time'), "%Y-%m-%d %H:%M:%S.%f")
        key = blink_time.strftime("%Y-%m-%d %H:%M")
        blink_count = blink_record_group_by_minute.get(key)
        if blink_count is None:
            blink_count = 1
        else:
            blink_count += 1
        blink_record_group_by_minute[key] = blink_count
    return dumps(blink_record_group_by_minute)


def fetch_exposure_data(user_id):
    User = Query()
    blink_records = blink_store_db.search(User.user_id == user_id)
    blink_record_group_by_day = {}
    for blink_record in blink_records:
        blink_time = datetime.strptime(blink_record.get('blink_time'), "%Y-%m-%d %H:%M:%S.%f")
        key = blink_time.strftime("%Y-%m-%d %H:%M")
        blink_count = blink_record_group_by_day.get(key)
        if blink_count is None:
            blink_count = 1
        else:
            blink_count += 1
        blink_record_group_by_day[key] = blink_count
    for key in blink_record_group_by_day:
        value = blink_record_group_by_day[key] * 100 / 1000
        blink_record_group_by_day[key] = value
    return dumps(blink_record_group_by_day)


def fetch_closeness_data(user_id):
    User = Query()
    closeness_records = closeness_store_db.search(User.user_id == user_id)
    closeness_record_group_by_day = {}
    for closeness_record in closeness_records:
        blink_time = datetime.strptime(closeness_record.get('close_time'), "%Y-%m-%d %H:%M:%S.%f")
        key = blink_time.strftime("%Y-%m-%d %H:%M")
        closeness_count = closeness_record_group_by_day.get(key)
        if closeness_count is None:
            closeness_count = 1
        else:
            closeness_count += 1
        closeness_record_group_by_day[key] = closeness_count
    for key in closeness_record_group_by_day:
        value = closeness_record_group_by_day[key] * 100 / 1000
        closeness_record_group_by_day[key] = value
    return dumps(closeness_record_group_by_day)


def fetch_touch_data(user_id):
    User = Query()
    touch_records = touch_store_db.find(User.user_id == user_id)
    touch_records_group_by_day = {}
    for touch_record in touch_records:
        blink_time = datetime.strptime(touch_record.get('touch_time'), "%Y-%m-%d %H:%M:%S.%f")
        key = blink_time.strftime("%Y-%m-%d %H:%M")
        touch_count = touch_records_group_by_day.get(key)
        if touch_count is None:
            touch_count = 1
        else:
            touch_count += 1
        touch_records_group_by_day[key] = touch_count
    for key in touch_records_group_by_day:
        value = touch_records_group_by_day[key] * 100 / 1000
        touch_records_group_by_day[key] = value
    return dumps(touch_records_group_by_day)
