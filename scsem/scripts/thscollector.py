#!/usr/bin/env python
import serial
import argparse
import time
import sys
import json

from influxdb import InfluxDBClient

class dbWrapper:

    def __init__(self,host, port,user, password, dbname, dbuser, dbpss):
        """Instantiate a connection to the InfluxDB."""
        self.client = InfluxDBClient(host, port, user, password,dbname)

        print("Create database: " + dbname)
        self.client.create_database(dbname)

        print("Create a retention policy")
        self.client.create_retention_policy('awesome_policy', '3d', 3,default=True)

        print("Switch user: " + dbuser)
        self.client.switch_user(dbuser, dbpss)


    def addData(self, data):
        try: 
          json_body = data
          self.client.write_points(json_body)
        except: 
          print "Unexpected error inserting in DB:", sys.exc_info()[0]


class btWrapper:

    def __init__(self,port,speed,timeout):
      self.port=port
      self.speed=speed
      self.timeout=timeout
      self.ser=None
      self.tryReconnect()

    def tryReconnect(self):
      print("Try reconnection to serial port:" + self.port)
      self.ser = serial.Serial(
        port=self.port,\
        baudrate=self.speed,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
        timeout=self.timeout)

    def getData(self):
      print("Getting data...")
      line=None     
      data=None
      i=0
      while line==None and i<2:
        i=i+1
        try:
          line = self.ser.readline()
          print("Got line, cool")
          break
        except KeyboardInterrupt:
          print("Ok ok, quitting")
          sys.exit(1)
        except: 
          self.tryReconnect()

      print("Checking line value...")
      if line is not None: 
        try:
          print("Something read yeah...:" + line)
          json_acceptable_string = line.replace("'", "\"")
          d = json.loads(json_acceptable_string)
          if d['status'] == "OK":
            print("Sensor OK Temperature:" + d['data']['t'])
            data= [{
              "measurement": "temperature",
              "tags": {
                  "sensor": d['id'],
              },
              "fields": {
                  "value": float(d['data']['t']),
              }},
              {
              "measurement": "humidity",
              "tags": {
                  "sensor": d['id'],
              },
              "fields": {
                  "value": float(d['data']['h']),
              }}] 
          else:
            print("Sensor KO")          
        except: 
          print("Error processing line as json, ignoring it")
      else:
        print("No data available on serial BT...:")

      return data

'''----------------------------------------------------------'''
'''----------------       M A I N         -------------------'''
'''----------------------------------------------------------'''

def main(host='localhost', port=8086):

    hdlDB=dbWrapper(host, port,
                    user = 'root',password = 'root',
                    dbname = 'db_emem',
                    dbuser = 'user_emem', dbpss = 'emem')       

    hdlBT=btWrapper(port='/dev/rfcomm0',speed=9600,timeout=20)

    while True:
       """ Get data from sensors """
       data = hdlBT.getData()
       """ Insert in DB """
       if data is not None:
          hdlDB.addData(data);

def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='Sensor data collector')
    parser.add_argument('--dbhost', type=str, required=False,
                        default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--dbport', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    return parser.parse_args()



if __name__ == '__main__':
    args = parse_args()
    main(host=args.dbhost, port=args.dbport)
