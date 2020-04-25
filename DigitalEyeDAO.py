from pymongo import MongoClient
from bson.json_util import dumps
from datetime import datetime, date

client = MongoClient('localhost', 27017)
db = client.digital_eyes
blink_store_db = db.blink_store


def store_blink(user_id):
    inserted_record = blink_store_db.insert_one({'user_id': user_id, 'blink_time': datetime.today()})
    print(inserted_record)
    return inserted_record


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
    return dumps(blink_record_group_by_day)