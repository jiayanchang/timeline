#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'jiayanchang'

import datetime
from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps

import config
#
# today = datetime.date.today()
#
# cursor = datetime.date(year=2017, month=3, day=1)
#
# while today >= cursor:
#
#     print "union select * from zhs_score_detail_%s where runner_child_id=%d and type_id = 2" % (cursor.strftime("%m%d"), 205804716)
#
#     cursor += datetime.timedelta(days=1)


client = MongoClient(config.timeline_mongo_host['host'])
db = client.test

"""
db.getCollection('test').update(
    {
         "userId":1,
         "$pull":
            {
                "values":
                {
                    "id":{'$in' : [1 , 2]}
                }

            }
    }

);

db.test.update({'userId': 4}, {'$pull': {'values': {'id': 1}}})
"""


for i in range(1, 100):
    data = []

    for j in range(1, 1000):
        data.append({"userId": 104657899,
            "circleUserNick": "淘气的瓠瓜fff",
            "userRole": 0,
            "avatar": "2017/03/24/19f05d54505ba86c5c7650100fe7ea6e/And/1490358587222-1244746321.jpg|2017/03/24/19f05d54505ba86c5c7650100fe7ea6e/And/1490358587222-1244746321.jpg@200h_200w",
            "mobile": "13336393314"
        })


    # print data
    db.test.update({'_id': ObjectId("58f1842a4e18178aa923d50b")}, {"$pushAll": {"users": data}})
    print i
