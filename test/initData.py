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

circlefile = open("circleId.txt")
userfile = open("prod_10w.txt")

line = userfile.readline()
fcircleId = circlefile.readline()

circleIds = []
while fcircleId:
    circleIds.append(fcircleId.replace('\n', ''))
    fcircleId = circlefile.readline()

users = []
while line:
    userId = line.split('\t')[0]
    users.append({"userId": userId, "userRole": 0, "mobile": str('18000000000'), "sex": -1, "joinTime": datetime.datetime.now()})
    line = userfile.readline()

userPages = []
print 'circleIds', len(circleIds)
print 'users', len(users)
for circleId in circleIds:
    index = 1
    temps = []
    for user in users:
        temps.append(user)
        if len(temps) < 10000:
            continue

        userPages.append({
            "circleId": circleId,
            "pageIndex": index,
            "pageCount": 10000,
            "users": temps
        })
        index += 1
        temps = []

print 'userPages', len(userPages)

# relatives = []
circles = []
for circleId in circleIds:
    circles.append({
        "circleId": circleId,
        "userRole": 0,
        "joinTime": datetime.datetime.now()
    })

# for user in users:
#     relatives.append({
#         "userId": int(user['userId']),
#         "circles": circles
#     })

# print 'relatives', len(relatives)


for userPage in userPages:
    db.circle_user_page.insert_one(userPage)

# for relative in relatives:
#     db.user_circle_relationship.insert_one(relative)
