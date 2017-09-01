#!/usr/bin/env python
import serial
import argparse
import time
import sys
import json
import subprocess
import os

from influxdb import InfluxDBClient


SensorsDirectory ={
  "Atico":     	{ "devType":"BT","btmac":"98:D3:32:20:FB:90","port":"/dev/rfcomm0","ITEMS":2},
#  "Dormitorio": { "devType":"BT","port":"/dev/rfcomm0","ITEM":1},
#  "Cocina":     { "devType":"LOCAL","gpio":23}
  }



'''----------------------------------------------------------'''
'''---------------- class database wrapper       ------------'''

class dbWrapper:

    def __init__(self,host, port,user, password, dbname, dbuser, dbpss):
      self.port=port
      self.host=host
      self.user=user
      self.password=password
      self.dbname=dbname
      self.dbuser=dbuser
      self.dbpss=dbpss
      self.tryReconnect()


    def tryReconnect(self):
      print("Try reconnection to database" + self.dbname)
      try:
        """Instantiate a connection to the InfluxDB."""
        self.client = InfluxDBClient(self.host, self.port, self.user, self.password,self.dbname)

        print("Create database: " + self.dbname)
        self.client.create_database(self.dbname)

        print("Create a retention policy")
        self.client.create_retention_policy('awesome_policy', '3d', 3,default=True)

        print("Switch user: " + self.dbuser)
        self.client.switch_user(self.dbuser, self.dbpss)
      except KeyboardInterrupt:
          print("Ok ok, quitting")
          sys.exit(1)
      except: 
          print "Unexpected error attempting to access to BD. It will be retried later.", sys.exc_info()[0]

    def addData(self, data):
        try: 
          json_body = data
          self.client.write_points(json_body)
        except KeyboardInterrupt:
          print("Ok ok, quitting")
          sys.exit(1)
        except: 
          print "Unexpected error inserting in DB:", sys.exc_info()[0]
          self.tryReconnect()

'''----------------------------------------------------------'''
'''---------------- class bluethoot dht22 wrapper------------'''

class btWrapper:

    def __init__(self,port,mac,speed,timeout):
      self.port=port
      self.speed=speed
      self.timeout=timeout
      self.ser=None
      self.mac=mac
      self.tryReconnect()

    def tryReconnect(self):
      print("Try to reconnect  btmac: {0} to port: {1}".format(self.mac,self.port))
      subprocess.call([os.path.dirname(__file__)+"/bindBTmac.sh",self.mac],shell=True)
      
      try:
        print("Try open serial port:" + self.port)
        self.ser = serial.Serial(
        port=self.port,\
        baudrate=self.speed,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
        timeout=self.timeout)
      except KeyboardInterrupt:
          print("Ok ok, quitting")
          sys.exit(1)
      except: 
          print "Unexpected error binding to btmac or accesing to serial port. It will be retried later.", sys.exc_info()[0]
          time.sleep(5)


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
'''---------------- class local dht22 wrapper ---------------'''

class localWrapper:

    def __init__(self,gpio):
      self.gpio=gpio
      self.tryReconnect()

    def tryReconnect(self):
      print("Try reconnection to local gpio:{0}".format(self.gpio))

    def getData(self):
      print("Getting data...")
      data=None
      return data

'''----------------------------------------------------------'''
'''----------------       M A I N         -------------------'''
'''----------------------------------------------------------'''

def main(host='localhost', port=8086):


    hdlDB=dbWrapper(host, port,
                    user = 'root',password = 'root',
                    dbname = 'db_emem',
                    dbuser = 'user_emem', dbpss = 'emem')       

    '''
    #Setup handlers for BT devices
    hdlBTs[]
    for item in SensorsDirectory:
      hdlBTs.append()


    for count in xrange(4):
    x = SimpleClass()
    x.attr = count
    simplelist.append(x)
    '''


    while True:
      for key,item in SensorsDirectory.items():
        data=None
        print("## Gathering data from sensor '{0}'".format(key))
        #Get data from sensors
        if not 'handler' in item:
          if item['devType'] == "BT":
            print("Creating BT object handler...")
            x=btWrapper(item['port'],item['btmac'],speed=9600,timeout=20)
          elif item['devType'] == "LOCAL":
            x=localWrapper(item['gpio'])
          else:
            print("Unknown sensor device type, ignoring it")
            continue
          item['handler']=x
        #tWrapperList.append(x)
        data = item['handler'].getData()
        # Insert in DB 
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
