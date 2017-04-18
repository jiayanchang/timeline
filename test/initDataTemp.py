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

print map(lambda x : x + x, [1,2,3,4])
