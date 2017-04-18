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

import sys

client = MongoClient(test_conf.timeline_mongo_host['host'])
db = client.circle_info


def get_circle_users(circleId, offset=0, limit=20):
    return db.circle_user_page.find({"circleId": circleId, "pageIndex": 1}, {"$slice": [offset, limit]})


if __name__ == '__main__':
    if len(sys.argv) > 1:
        limit = int(sys.argv[1])
        f = open('circleId.txt', 'r')
        circleId = f.readline()

        while circleId and limit > 1:
            print get_circle_users(circleId)
            limit -= 1
            circleId = f.readline()
