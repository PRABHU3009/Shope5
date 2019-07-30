from configparser import ConfigParser, ExtendedInterpolation
import pymongo, os

cfg = ConfigParser(interpolation=ExtendedInterpolation())
cfg.read('config.ini')
# uri=cfg['ENV_VARIABLES']['MONGO_URI']
uri=os.os.environ['MONGO_URI']

client = pymongo.MongoClient(uri,connectTimeoutMS=30000)
db=client.get_database("shopify_orders")
ordereditems= db['ordereditems']

def getRecords():
	list=[]
	for item in ordereditems.find():
		list.append(item)
	return list

def getRecord(id):
    record = ordereditems.find_one({"id" : id})
    return record

def updateRecord(record, updates):
    ordereditems.update_one({'id': record['id']},{
                              '$set': updates
                              }, upsert=False)
def pushRecord(record):
    ordereditems.insert_one(record)
