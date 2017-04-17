#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'jiayanchang'

from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps
import threading

import random
import test.test_conf
import datetime
import time

users = test.test_conf.users
circles = test.test_conf.circles

def update():
    client = MongoClient(test.test_conf.timeline_mongo_host['host'])
    # client.circle_info.authenticate('admin', 'admin', mechanism='SCRAM-SHA-1')
    db = client.circle_info

    timestap = datetime.datetime.now()
    for i in range(0, 10):
        user = random.choice(users)
        circle = random.choice(circles)
        db.circle_user_page.update({"circleId": circle['_id'], "pageIndex": 1},
                               {"$push": {"users": {"userId": user[0], "userRole": 0, "mobile": str(user[1]), "sex": -1, "joinTime": datetime.datetime.now()}}})

        now = datetime.datetime.now()
        print (now - timestap).microseconds
        timestap = now

    time.sleep(0.5)
    update()


threads = []
for i in (0, 10000):
    threads.append(threading.Thread(target=update))


if __name__ == '__main__':

    for t in threads:
        t.setDaemon(True)
        t.start()
