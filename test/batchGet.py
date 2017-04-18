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

def get_circle_users(circleId):
    return db.circle_user_page.find({"circleId": circleId, "pageIndex": 1}, {"$slice": [0, 20]})



for i in (0, 10000):
    print i
