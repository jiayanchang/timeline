#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'jiayanchang'

from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps
import threading

import random
import test_conf
import datetime
import time


client = MongoClient(test_conf.timeline_mongo_host['host'])
db = client.circle_info

def clearUserRelatives(users):
    for userId in users:
        db.user_circle_relationship.delete_many({"userId":userId})


def insertUserToCircle(circleId, users, index):
    # record = db.circle_user_page.find({"circleId": ObjectId(circleId)}, {"circleId": 1}).limit(1)
    # if len(list(record)) > 0:
    # db.circle_user_page.delete_many({"circleId": ObjectId(circleId), "pageIndex": index})

    db.circle_user_page.insert_one({
        "circleId": circleId,
        "pageIndex": index,
        "pageCount": 10000,
        "users": users
    })


    for userId in users:
        record = db.user_circle_relationship.find({"userId": userId}, {"userId": 1}).limit(1)
        if len(list(record)) > 0:
            db.user_circle_relationship.update_one({"userId": userId}, {"$push": {"circles": {
                "circleId": circleId,
                "userRole": 0,
                "joinTime": datetime.datetime.now()
            }}}, False)
        else:
            db.user_circle_relationship.insert_one({
                "userId": userId,
                "circles": [
                    {
                        "circleId": circleId,
                        "userRole": 0,
                        "joinTime": datetime.datetime.now()
                    }
                ]
            })

    print circleId, index


circlefile = open("circleId.txt")
userfile = open("prod_10w.txt")

line = userfile.readline()
circleId = circlefile.readline()

while circleId:
    users = []
    index = 1
    while line:
        userId = line.split('\t')[0]
        users.append({"userId": userId, "userRole": 0, "mobile": str('18000000000'), "sex": -1, "joinTime": datetime.datetime.now()})
        line = userfile.readline()

        if len(users) < 10000:
            continue

        insertUserToCircle(circleId.replace('\n', ''), users, index)
        index += 1
        users = []

    circleId = circlefile.readline()

