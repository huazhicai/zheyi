import decimal
import time
import threading
from datetime import datetime, timedelta

from config.xue_config import system_tag_id

# mongo数据库配置
from utils import logger
from xuetou import multi_thread, single_thread, cursor, db, collection

logger = logger.getLogger('main')

# 索引数据表
collect_index = db['update_reference']

"""
bingshi, DateTime
DialyseRoute, Modify_Time
DialyseScheme, Modify_Time
CRRT
"""


class MyThreadCycle(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        cycle_count = 1
        while True:
            logger.info('Starting cycle {}!'.format(cycle_count))
            record_time = datetime.now()
            record_time_str = record_time.strftime('%Y-%m-%d %H:%M:%S')
            ids = self.get_patients_id()
            new_ids = self.filter_ids(ids)

            multi_thread(new_ids)
            collect_index.update_one({'_id': system_tag_id}, {'$set': {'update_time': record_time_str}}, upsert=True)
            logger.info('Cycle {} Done!'.format(cycle_count))
            cycle_count += 1

            if datetime.now() < record_time + timedelta(minutes=1):
                dt = record_time + timedelta(minutes=1) - datetime.now()
                time.sleep(dt.seconds)

    def get_patients_id(self):
        last_update_time = collect_index.find_one({'_id': system_tag_id}).get('update_time')
        init_time = collect_index.find_one({'_id': system_tag_id}).get('init_time')
        assert last_update_time
        if last_update_time == init_time:  # 存在modify_time为空，所以第一次都取
            sql = 'select id, modify_time from Patient'
        else:
            sql = "select id, modify_time from Patient where modify_time > '{}' ".format(last_update_time)

        cursor.execute(sql)
        row = cursor.fetchone()
        ids = []
        while row:
            id, time = row
            if isinstance(id, decimal.Decimal):
                id = int(id)
            if isinstance(time, datetime):
                time = time.strftime('%Y-%m-%d %H:%M:%S')
            ids.append([id, time])
            row = cursor.fetchone()
        return ids

    def filter_ids(self, ids):
        """过滤已经更新过的"""
        new_ids = []
        for id in ids:
            one_data = collection.find_one({'_id': id})
            if one_data and id[1] < one_data.get('modify_time'):
                continue
            new_ids.append(id[0])
        return new_ids


class ListenEventThread(threading.Thread):

    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            patient_id = collect_index.find_one({'_id': system_tag_id}).get('patient_id')
            if patient_id:
                logger.info('web搜索更新开始：patient_id={}'.format(patient_id))
                single_thread(patient_id)
                collect_index.update_one({'_id': system_tag_id}, {'$set': {'patient_id': None}}, upsert=True)
                logger.info('web搜索更新成功: patient_id={}'.format(patient_id))
            time.sleep(1)


if __name__ == '__main__':
    cycle_thread = MyThreadCycle()
    listen_thread = ListenEventThread()

    cycle_thread.start()
    listen_thread.start()

    cycle_thread.join()
    listen_thread.join()
