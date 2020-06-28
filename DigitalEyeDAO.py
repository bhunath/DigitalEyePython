import os
from datetime import datetime
from bson.json_util import dumps
from tinydb import TinyDB, Query
from tinydb.table import Document
import threading
from DigitalEyeUtils import DigitalEyeUtils

threadLock_blink = threading.Lock()
threadLock_closeness = threading.Lock()
threadLock_touch = threading.Lock()
exposureLock_touch = threading.Lock()
dirname = os.getcwd()
utils = DigitalEyeUtils()
db_blink_store = TinyDB(dirname + '/blink_db.json')
db_closeness_store = TinyDB(dirname + '/closeness_db.json')
db_touch_store = TinyDB(dirname + '/touch_db.json')
db_exposure_store = TinyDB(dirname + '/exposure_db.json')
exposure_store_db = db_exposure_store.table('exposure_store')
db_settings = TinyDB(dirname + '/settings_db.json')
blink_store_db = db_blink_store.table('blink_store')
closeness_store_db = db_closeness_store.table('closeness_store')
touch_store_db = db_touch_store.table('touch_store')
settings_db = db_settings.table('user_settings')


def store_blink(user_id):
    try:
        threadLock_blink.acquire()
        inserted_record = blink_store_db.insert({'user_id': user_id, 'blink_time': datetime.today().__str__()})
        threadLock_blink.release()
        #print(inserted_record)
        return inserted_record
    except:
        print("Error Occurred while storing blink Record")


def store_exposure(user_id):
    try:
        exposureLock_touch.acquire()
        inserted_record = exposure_store_db.insert({'user_id': user_id, 'exposure_time': datetime.today().__str__()})
        exposureLock_touch.release()
        return inserted_record
    except:
        print("Error Occurred while storing blink Record")


def store_user_settings(user_id,settings):
    print('settings_arr')
    try:
        current_settings = settings_db.get(doc_id=user_id)
        if current_settings is not None :
            settings_db.update(settings,doc_ids=[user_id])
        else :
            settings_db.insert(Document(settings,doc_id=user_id))
        print('returning')
        utils.user_settings_updated(settings)
        return settings
    except:
        print("Error Occurred while storing settings")


def fetch_user_settings(user_id):
    try:
        settings = None
        current_settings = settings_db.get(doc_id=user_id)
        if current_settings is not None :
            settings = current_settings
        return settings
    except:
        print("Error Occurred while fetching settings")



def store_touch(user_id):
    try:
        threadLock_touch.acquire()
        inserted_record = touch_store_db.insert({'user_id': user_id, 'touch_time': datetime.today().__str__()})
        threadLock_touch.release()
        #print(inserted_record)
        return "inserted_record"
    except:
        print("Error Occurred in Storing Touch")


def store_closeness(user_id):
    try:
        threadLock_closeness.acquire()
        closeness_record = closeness_store_db.insert({'user_id': user_id, 'close_time': datetime.today().__str__()})
        threadLock_closeness.release()
        #print('Eye is Close Record', closeness_record)
        return "closeness_record"
    except:
        print("Error Occurred while storing closeness Record")


def get_group_by_format(groupBy):
    if "minute" == groupBy:
        return "%H:%M"
    if "hour" == groupBy:
        return "%H"
    if "day" == groupBy:
        return "%Y-%m-%d"


def fetch_blink_report_per_minute(user_id, groupBy):
    User = Query()
    blink_records = blink_store_db.search(User.user_id == user_id)
    blink_record_group_by_minute = {}
    for blink_record in blink_records:
        blink_time = datetime.strptime(blink_record.get('blink_time'), "%Y-%m-%d %H:%M:%S.%f")
        day = blink_time.strftime(get_group_by_format('day'))
        time = blink_time.strftime(get_group_by_format(groupBy))
        date_data = blink_record_group_by_minute.get(day)
        if date_data is None:
            time_data = {time: 1}
            blink_record_group_by_minute[day] = time_data
        else:
            time_data = date_data.get(time)
            if time_data is not None:
                time_data += 1
                date_data[time] = time_data
                blink_record_group_by_minute[day] = date_data
            else:
                time_data = {time: 1}
                blink_record_group_by_minute[day].update(time_data)
    return dumps(blink_record_group_by_minute)


def fetch_exposure_data(user_id, groupBy):
    User = Query()
    blink_records = exposure_store_db.search(User.user_id == user_id)
    blink_record_group_by_minute = {}
    for blink_record in blink_records:
        blink_time = datetime.strptime(blink_record.get('exposure_time'), "%Y-%m-%d %H:%M:%S.%f")
        day = blink_time.strftime(get_group_by_format('day'))
        time = blink_time.strftime(get_group_by_format(groupBy))
        date_data = blink_record_group_by_minute.get(day)
        if date_data is None:
            time_data = {time: 1}
            blink_record_group_by_minute[day] = time_data
        else:
            time_data = date_data.get(time)
            if time_data is not None:
                time_data += 1
                date_data[time] = time_data
                blink_record_group_by_minute[day] = date_data
            else:
                time_data = {time: 1}
                blink_record_group_by_minute[day].update(time_data)
    return dumps(blink_record_group_by_minute)


def fetch_closeness_data(user_id, groupBy):
    User = Query()
    closeness_records = closeness_store_db.search(User.user_id == user_id)
    closeness_record_group_by_day = {}
    for blink_record in closeness_records:
        blink_time = datetime.strptime(blink_record.get('close_time'), "%Y-%m-%d %H:%M:%S.%f")
        day = blink_time.strftime(get_group_by_format('day'))
        time = blink_time.strftime(get_group_by_format(groupBy))
        date_data = closeness_record_group_by_day.get(day)
        if date_data is None:
            time_data = {time: 10}
            closeness_record_group_by_day[day] = time_data
        else:
            time_data = date_data.get(time)
            if time_data is not None:
                time_data += 10
                date_data[time] = time_data
                closeness_record_group_by_day[day] = date_data
            else:
                time_data = {time: 10}
                closeness_record_group_by_day[day].update(time_data)
    return dumps(closeness_record_group_by_day)


def fetch_touch_data(user_id, groupBy):
    User = Query()
    touch_records = touch_store_db.search(User.user_id == user_id)
    touch_records_group_by_day = {}
    for touch_record in touch_records:
        blink_time = datetime.strptime(touch_record.get('touch_time'), "%Y-%m-%d %H:%M:%S.%f")
        day = blink_time.strftime(get_group_by_format('day'))
        time = blink_time.strftime(get_group_by_format(groupBy))
        date_data = touch_records_group_by_day.get(day)
        if date_data is None:
            time_data = {time: 1}
            touch_records_group_by_day[day] = time_data
        else:
            time_data = date_data.get(time)
            if time_data is not None:
                time_data += 1
                date_data[time] = time_data
                touch_records_group_by_day[day] = date_data
            else:
                time_data = {time: 1}
                touch_records_group_by_day[day].update(time_data)
    return dumps(touch_records_group_by_day)
