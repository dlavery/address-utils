import configparser
import pymongo
from pymongo import MongoClient
from addressutils import PAFattrs
from addressutils import paf_to_lines
from addressutils import phonetic

def setup(db):
    db.addresses.create_index([('phonetic', 1)], unique=False, sparse=True)
    db.addresses.create_index([('postcode', 1)], unique=False, sparse=True)
    db.addresses.create_index([('UDPRN', 1)], unique=True, sparse=True)

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('addressutils.cfg')
    client = MongoClient(config['DATABASE']['dbURI'])
    db = client[config['DATABASE']['dbName']]
    setup(db)
    address = {}
    with open('CSV PAF.csv') as f:
        for line in f:
            cols = line[:-1].split(',')
            address = {PAFattrs[i]: cols[i] for i in range(len(cols)) if cols[i]}
            lines = paf_to_lines(address)
            address['phonetic'] = phonetic(lines[0] + ' ' + lines[1])
            address_id = db.addresses.insert(address)
