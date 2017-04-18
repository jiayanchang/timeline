#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'jiayanchang'

from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps
from threading import Thread
import Queue

import random
import test_conf
import datetime
import time


class InsertWorker(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
        self.client = MongoClient(test_conf.timeline_mongo_host['host'])
        self.db = self.client.circle_info

    def run(self):
        while True:
            page = self.queue.get()
            self.db.circle_user_page.insert_one(page)
            # print relative['userId'], '\t'


def getPages():
    # global circlefile, userfile, line, fcircleId, circleIds, users, userId, userPages, circleId, index, temps, user, circles
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
    return userPages


def main():
    pages = getPages()
    queue = Queue.Queue(len(pages))
    for x in range(0, 8):
        worker = InsertWorker(queue)
        worker.setDaemon(True)
        worker.start()

    for page in pages:
        queue.put(page)

    queue.join()


if __name__ == '__main__':
    main()
