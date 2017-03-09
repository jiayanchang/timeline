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
    db.user_follow.insert(json)

def get(user_id):
    return db.user_follow.find_one({"user_id": user_id}).denny()

def get_friends(user_id, offset=0, limit=10):
    return db.user_follow.find_one({"user_id":user_id}, {"f_ids":{"$slice":[offset, limit]}})

def is_friend(user_id, to_id):
    return dumps(db.user_follow.find(
                {"user_id":user_id, "f_ids.to_id":to_id},
                {"_id":0, "f_ids.$":1}
            ))

insert_data = {"user_id": 1}

def push(mongoid, json):
    db.user_follow.update({'_id': mongoid}, {"$push":json})


# insert(insert_data)
def init_data():
    for i in range(0, 10000):
        push(ObjectId("58be4ee9c3666e2a75369029"), {"f_ids":{"to_id":100001 + i, "time":datetime.datetime.now()}})


# db.user_follow.find({"user_id":1, "f_ids.to_id":100000})

print get_friends(1, 10000, 20)
# print is_friend(1, 200000)
