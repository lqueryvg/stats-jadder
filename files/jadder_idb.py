#!/usr/bin/env python

#import statsd
from influxdb import InfluxDBClient
import datetime

from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps

args = None
def get_options():
    import argparse
    parser = argparse.\
        ArgumentParser(description='simple rest test with push to statsd')
    parser.add_argument('--port', required=False, default=5000)
    parser.add_argument('--influxdb_host', required=False, default='localhost')
    parser.add_argument('--influxdb_port', required=False, default=8086)
    global args
    args = parser.parse_args()

get_options()

app = Flask(__name__)
api = Api(app)

my_total_uploads = 0
client = InfluxDBClient(args.influxdb_host, args.influxdb_port, 'root', 'root', 'example')
#c = statsd.StatsClient(args.statsd_host, args.statsd_port)

class Get(Resource):
    def get(self):
        return {'my_total_uploads': my_total_uploads}

class Add(Resource):
    def get(self):
        global my_total_uploads
        my_total_uploads = my_total_uploads + 1
        #c.incr('total_uploads')

        now = datetime.datetime.today()
        point = {
            "measurement": 'uploads',
            #"time": int(now.strftime('%s')),
            "fields": { "value": 1 }
        }

        client.write_points([point])

        return {'my_total_uploads': my_total_uploads}
 
api.add_resource(Add, '/add')
api.add_resource(Get, '/get')

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=args.port)

