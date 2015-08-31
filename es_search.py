from elasticsearch import Elasticsearch
import splunk.Intersplunk
import sys
import datetime
import time

username = ''
password = ''
servername = ''

es = Elasticsearch(['https://{0}:{1}@{2}:9200'.format(username, password, servername)], verify_certs=False)

es_search = es.search(index="eventlog*", body={"query": {"match": {'Opcode':'Info'}}})

row = {}
intersplunk_results = []

for hit in es_search['hits']['hits']:
    row = hit['_source']

    row['_time'] = int(time.mktime(time.strptime(((hit['_source']['@timestamp']).partition('.')[0]), '%Y-%m-%dT%H:%M:%S')))
    row['index'] = hit['_index']
    row['sourcetype'] = hit['_type']
    intersplunk_results.append(row)
    row['_raw'] = row
    row = {}

splunk.Intersplunk.outputStreamResults(intersplunk_results)
