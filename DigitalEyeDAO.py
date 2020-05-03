from pymongo import MongoClient
from bson.json_util import dumps
from datetime import datetime, date

client = MongoClient('localhost', 27017)
db = client.digital_eyes
blink_store_db = db.blink_store
closeness_store_db = db.closeness_store
touch_store_db = db.touch_store


def store_blink(user_id):
    inserted_record = blink_store_db.insert_one({'user_id': user_id, 'blink_time': datetime.today()})
    print(inserted_record)
    return inserted_record


def store_touch(user_id):
    inserted_record = touch_store_db.insert_one({'user_id': user_id, 'touch_time': datetime.today()})
    print(inserted_record)
    return "inserted_record"


def store_closeness(user_id):
    closeness_record = closeness_store_db.insert_one({'user_id': user_id, 'close_time': datetime.today()})
    print('Eye is Close Record',closeness_record)
    return closeness_record


def fetch_blink_report_per_minute(user_id):
    blink_records = blink_store_db.find({'user_id': user_id})
    blink_record_group_by_minute = {};
    for blink_record in blink_records:
        key = '{0:%d}-{0:%m}-{0:%Y},{0:%H}:{0:%M}'.format(blink_record.get('blink_time'))
        blink_count = blink_record_group_by_minute.get(key)
        if blink_count is None:
            blink_count = 1
        else:
            blink_count += 1
        blink_record_group_by_minute[key] = blink_count
    return dumps(blink_record_group_by_minute)


def fetch_exposure_data(user_id):
    blink_records = blink_store_db.find({'user_id': user_id})
    blink_record_group_by_day = {};
    for blink_record in blink_records:
        key = '{0:%d}-{0:%m}-{0:%Y}'.format(blink_record.get('blink_time'))
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
    closeness_records = closeness_store_db.find({'user_id': user_id})
    closeness_record_group_by_day = {}
    for closeness_record in closeness_records:
        key = '{0:%d}-{0:%m}-{0:%Y},{0:%H}:{0:%M}'.format(closeness_record.get('close_time'))
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
    touch_records = touch_store_db.find({'user_id': user_id})
    touch_records_group_by_day = {}
    for touch_record in touch_records:
        key = '{0:%d}-{0:%m}-{0:%Y},{0:%H}:{0:%M}'.format(touch_record.get('touch_time'))
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
