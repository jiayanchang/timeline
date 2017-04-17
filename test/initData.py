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


client = MongoClient(test.test_conf.timeline_mongo_host['host'])
db = client.circle_info


def insertUserToCircle(circleId, users):

    record = db.circle_user_page.find({"circleId": ObjectId(circleId)}, {"circleId": 1}).limit(1)
    if record:
        db.circle_user_page.update({"circleId": ObjectId(circleId), "pageIndex": 1},
                                   {"$push": {"users": users}})
    else:
        db.circle_user_page.insert({
            "circleId": "58ede8ad0cf28b716ec4cb02",
            "pageIndex": 1,
            "pageCount": 10000,
            "users": users
        })


    record = db.user_circle_relationship.find({"userId": userId}).limit(1)

    if record:
        db.user_circle_relationship.update(({"userId": userId}, {"$push": {"circles": {
            "circleId": circleId,
            "userRole": 0,
            "joinTime": datetime.datetime.now()
        }}}))
    else:
        db.user_circle_relationship.insert({
            "userId": userId,
            "circles": [
                {
                    "circleId": circleId,
                    "userRole": 0,
                    "joinTime": datetime.datetime.now()
                }
            ]
        })


circlefile = open("circleid.txt")
userfile = open("prod_10w.txt")
line = userfile.readline()

users = []
while line:
    userId = line.split('\t')[0]
    users.append({"userId": userId, "userRole": 0, "mobile": str('18000000000'), "sex": -1, "joinTime": datetime.datetime.now()})
    line = userfile.readline()

    if len(users) < 10000:
        continue

    insertUserToCircle(users)

    print len(users)
    users = []


    # circleId = circlefile.readline()
    # while circleId:
    # insertUserToCircle(circleId, userId)
    #         circleId = userfile.readline()