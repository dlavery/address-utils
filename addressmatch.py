import configparser
import pymongo
import re
import sys
from pymongo import MongoClient
from addressutils import separate_postcode
from addressutils import normalise
from addressutils import phonetic
from addressutils import paf_to_lines
from addressutils import single_line
from addressutils import normalise
from addressutils import expand_abbreviations
from addressutils import remove_stopwords
from addressutils import strip_spaces
from addressutils import jaccard_index

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('addressutils.cfg')
    client = MongoClient(config['DATABASE']['dbURI'])
    db = client[config['DATABASE']['dbName']]

    if len(sys.argv) < 2:
        print('>> PLEASE PROVIDE AN ADDRESS TO MATCH')
        sys.exit(0)

    to_match = sys.argv[1]
    res = separate_postcode(normalise(to_match))
    postcode = res[1]
    to_match = res[0]
    if postcode:
        addresses = db.addresses.find({'postcode': postcode})
    else:
        res = re.split('\W+', to_match)
        address = ' '.join(res[:min(len(res), 4)])
        addresses = db.addresses.find({'phonetic': {'$regex': '^' + phonetic(address)}})

    to_match = strip_spaces(remove_stopwords(expand_abbreviations(to_match)))
    best_jaccard = 0
    best_match = list()
    for address in addresses:
        lines = paf_to_lines(address)
        line = separate_postcode(normalise(single_line(lines)))
        line = strip_spaces(remove_stopwords(expand_abbreviations(line[0])))
        idx = jaccard_index(to_match, line)
        if idx > best_jaccard:
            best_jaccard = idx
            best_match = list()
            best_match.append(address)
        elif idx == best_jaccard:
            best_match.append(address)

    if len(best_match) == 1:
        print(">> BEST MATCH")
        print(best_match[0])
    elif len(best_match) == 0:
        print(">> NO MATCH")
    else:
        print(">> MULTIPLE MATCHES")
        for match in best_match:
            print(match)
