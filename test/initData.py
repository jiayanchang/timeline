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
userDetails = []
print 'circleIds', len(circleIds)
print 'users', len(users)
i = 1
for circleId in circleIds:
    for user in users:
        userPages.append({
            "circleId": circleId,
            "userId": int(user['userId'])
        })

        userDetails.append({
            "_class" : "com.bbtree.service.circle.vo.CircleUserDetail",
            "circleId" : circleId,
            "userId" : int(user['userId']),
            "circleUserNick" : "勤快" + str(i),
            "userRole" : 0,
            "avatar" : "2017/04/11/2b5ad69085de66b344bd4867c205ad5d/ios/1491901291399095.jpg|2017/04/11/2b5ad69085de66b344bd4867c205ad5d/ios/1491901291399095.jpg@200h_200w|2017/04/11/2b5ad69085de66b344bd4867c205ad5d/ios/1491901291399095.jpg@544h_545w",
            "mobile" : "15201153830",
            "sex" : 1,
            "joinTime" : user['joinTime']
        })

        i += 1

print 'userPages', len(userPages)


for userPage in userPages:
    db.cu_relationship.insert_one(userPage)

for userDetail in userDetails:
    db.cu_detail.insert_one(userDetail)

# for relative in relatives:
#     db.user_circle_relationship.insert_one(relative)
