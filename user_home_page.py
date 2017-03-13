#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'jiayanchang'

from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps

import config
import datetime


client = MongoClient(config.timeline_mongo_host['host'])
db = client.circle


def insert(json):
    db.user_home_page.insert(json)

def get(user_id):
    return db.user_home_page.find_one({"user_id": user_id}).denny()

def circles(user_id, offset=0, limit=10):
    return db.user_home_page.find_one({"user_id":user_id})

def members(circle_id):
    db.user_home_page.find({"circles.circle_id": circle_id})

def member(user_id, circle_id):
    return dumps(db.user_home_page.find(
                {"user_id":user_id, "circles.circle_id":circle_id},
                {"_id":0, "f_ids.$":1}
            ))

insert_data = {"user_id": 1}

def push(mongoid, json):
    db.user_home_page.update({'_id': mongoid}, {"$push":json})


# insert(insert_data)
def init_data():

    for i in range(1, 10):
        data = {"user_id": i, "timelines": []}
        recs = []
        for j in range(1, 5000):
            # recs.append({"circle_id": j, "nick": "nick" + str(j), "join_type": 0, "role": 0 if j % 10 == 0 else 1, "time": datetime.datetime.now()})
            recs.append(1000000 + j)
        data.update({"timelines": recs})
        # print data
        insert(data)

init_data()
# db.user_home_page.find({"user_id":1, "f_ids.to_id":100000})

# print get_friends(1,10000,20)
# print is_friend(1, 200000)
