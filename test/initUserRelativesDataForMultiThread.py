#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'jiayanchang'

from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps
from threading import Thread

import random
import test_conf
import datetime
import time
from queue import Queue


class InsertWorker(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
        self.client = MongoClient(test_conf.timeline_mongo_host['host'])
        self.db = self.client.circle_info

    def run(self):
        while True:
            relative = self.queue.get()
            self.db.user_circle_relationship.insert_one(relative)
            # print relative['userId'], '\t'


def initRelationData():
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

    # userPages = []
    print 'circleIds', len(circleIds)
    print 'users', len(users)
    relatives = []
    circles = []
    for circleId in circleIds:
        circles.append({
            "circleId": circleId,
            "userRole": 0,
            "joinTime": datetime.datetime.now()
        })
    for user in users:
        relatives.append({
            "userId": int(user['userId']),
            "circles": circles
        })
    print 'relatives', len(relatives)
    return relatives


def main():
    relatives = initRelationData()

    queue = Queue()
    for x in range(0, 8):
        worker = InsertWorker(queue)
        # 将daemon设置为True将会使主线程退出，即使worker都阻塞了
        worker.setDaemon(True)
        worker.start()

    for relative in relatives:
        queue.put(relative)

    # 让主线程等待队列完成所有的任务
    queue.join()


if __name__ == '__main__':
    main()