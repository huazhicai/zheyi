# _*_ coding: utf-8 _*_

from pymongo import MongoClient
import os
import shutil
import tarfile
from collections import OrderedDict


class MongoOperator:
    def __init__(self, host, port, db_name, username, password, collection):
        self.client = MongoClient(host=host, port=port)
        self.db = self.client.get_database(db_name)
        self.authen = self.db.authenticate(username, password)
        self.collection = self.db.get_collection(collection)
        self.users_id = set()
        self.micons = OrderedDict()


    def get_owners(self):
        for user in self.collection.find():
            try:
                self.users_id.add(user["owner"])
            except:
                print "no"
        return self.users_id

    def get_micons(self):
        while len(self.users_id) > 0:
            uid = self.users_id.pop()
            micons = []
            for micon in self.collection.find({"owner": uid, "current_phoneres.phoneprocessinfo.restag": "A"}):
                try:
                    micons.append(micon["current_phoneres"]["micon"])
                except:
                    print "micon not exits"

            res = {uid: micons}
            self.micons.update(res)
        return self.micons

    def make_dir(self, uid):
        if not os.path.exists('/home/logfile/%s/A/' % uid):
            os.makedirs('/home/logfile/%s/A/' % uid)
        return '/home/logfile/%s/A/' % uid


    def copy_file(self, src_dir, target_dir):
        if os.path.exists(src_dir) and os.path.isdir(src_dir):
            # pattern = re.compile(r"\d+\.log")
            path_dir = os.listdir(src_dir)
            if len(path_dir)>0:
                obj_file = sorted(path_dir, key=len).pop()
                shutil.copy(src_dir+obj_file, target_dir)
                print 'ok'
            # shutil.rmtree(filepath)
        else:
            print ("%s not exists." % src_dir)


if __name__ == '__main__':

    db = MongoOperator('mongodb://yfsrobot:yfsrobotksdw1212@dds-bp12f2cb45820f042.mongodb.rds.aliyuncs.com:3717,dds-bp12f2cb45820f041.mongodb.rds.aliyuncs.com:3717/yfsrobot?replicaSet=mgset-2562725', 
        27017, 'yfsrobot', 'yfsrobot', 'yfsrobotksdw1212', 'phoneplan')
    db.get_owners()
    obj_data = db.get_micons()
    for key, value in obj_data.items():
        uid = key
        target_dir = db.make_dir(uid)
        micon = value
        for icon in micon:
            src_dir = "/recodedata/recordfile/%s/" % icon
            db.copy_file(src_dir, target_dir)
    db.close()