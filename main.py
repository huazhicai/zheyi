from multiprocessing.pool import Pool
import time


# def get_patients_id():
#     collect = db.update_reference
#     update_time = collect.find_one({'_id': system_tag_id}).get('update_time')
#     init_time = collect.find_one({'_id': system_tag_id}).get('init_time')
#     assert update_time
#     if update_time == init_time:
#         sql = 'select id from Patient'
#     else:
#         sql = "select id from Patient where modify_time > '{}' ".format(update_time)
#     cursor.execute(sql)
#     row = cursor.fetchone()
#     ids = []
#     while row:
#         ids.append(int(row[0]))
#         row = cursor.fetchone()
#     return ids
#
#
# def scheduler():
#     pool = Pool(8)
#     while True:
#         ids = get_patients_id()
#         if ids:
#             logger.info('Starting crawler!')
#             record_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             record_time = '2020-11-04 21:29:20'
#             pool.map(main, ids)
#             pool.close()
#             pool.join()
#             collect = db.update_reference
#             collect.update_one({'_id': system_tag_id}, {'$set': {'update_time': record_time}}, upsert=True)
#             logger.info('crawler end!')
#         time.sleep(3)
