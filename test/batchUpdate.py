#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'jiayanchang'

from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps
import random
import test.test_conf
import datetime


client = MongoClient(test.test_conf.timeline_mongo_host['host'])
db = client.circle_info
users = test.test_conf.users
circles = test.test_conf.circles


timestap = datetime.datetime.now()
for i in range(0, 1000):
    user = random.choice(users)
    circle = random.choice(circles)
    db.circle_user_page.update({"circleId": circle['_id'], "pageIndex": 1},
                           {"$push": {"users": {"userId": user[0], "userRole": 0, "mobile": str(user[1]), "sex": -1, "joinTime": datetime.datetime.now()}}})

    now = datetime.datetime.now()
    print now - timestap
    timestap = now

