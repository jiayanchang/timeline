from pymongo import MongoClient
import config


def getClient():
	client = MongoClient(config.timeline_mongo_host["host"])

