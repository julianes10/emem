#!/usr/bin/env python
import argparse
import time
import sys
import json
import subprocess
import os
import platform
import threading

from collectorCommon import *
from dbwrapper import *
from btwrapper import *
from localdhtwrapper import *

SensorsDirectory ={
  "Atico":     	{ "devType":"BT",
                  "btmac":"98:D3:32:20:FB:90","port":"/dev/rfcomm0",
                  "subnames": { 'id1': "Terraza Interior", 'id2':"Terraza Exterior"}
                },
#  "Dormitorio": { "devType":"BT","port":"/dev/rfcomm0","ITEM":1},
  "Cocina":     { "devType":"LOCAL","gpio":4}
  }





'''----------------------------------------------------------'''
'''----------------       M A I N         -------------------'''
'''----------------------------------------------------------'''

def main(host='localhost', port=8086,lc=False):
  print('SCSEM-start -----------------------------')   
  internalLogger.critical('SCSEM-start -----------------------------')        

  if lc==True:
      launchContainers()

  try:    
    hdlDB=dbWrapper(host, port,
                    user = 'root',password = 'root',
                    dbname = 'db_emem',
                    dbuser = 'user_emem', dbpss = 'emem') 

    for key,item in SensorsDirectory.items():
      if item['devType'] == "BT":
           internalLogger.debug("Creating BT object handler...")
           x=btWrapper(key,item,speed=9600,timeout=20)
           x.tryReconnect()
      elif item['devType'] == "LOCAL":
           internalLogger.debug("Creating local DHT object handler...")
           x=localDhtWrapper(key,item)
      else:
           internalLogger.error("Unknown sensor device type, ignoring it")
           continue
      item['handler']=x
      sensorTask=threading.Thread(target=sensor_task,args=(key,item,hdlDB,),name=key)
      sensorTask.daemon = True
      sensorTask.start()
      
    while True:
        time.sleep(1) 

  except Exception as e:
    e = sys.exc_info()[0]
    internalLogger.critical('Error: Exception unprocessed properly. Exiting')
    einternalLogger.exception(e)  
    print('SCSEM-General exeception captured. See ssms.log:{0}',format(LOGFILE_DEV))        
      
  internalLogger.critical('SCSEM-end -----------------------------')        
  print('SCSEM-end -----------------------------')


'''----------------------------------------------------------'''
'''----------------       launchContainers-------------------'''
def launchContainers():
      try:
        internalLogger.info("Relaunching containers...")
        p=subprocess.Popen([EMEM_DEPLOY_DIR+'/scsem/scripts/launchContainers.sh','verbose'])      
        internalLogger.debug("Script for launching container started  with popen:")
      except KeyboardInterrupt:
        print("Ok ok, quitting")
        sys.exit(1)
      except Exception as e:
        e = sys.exc_info()[0]
        internalLogger.error('Unexpected error launching containers. Not recovery so far TODO.')
        einternalLogger.exception(e)  
        time.sleep(5)
        sys.exit(1)
'''----------------------------------------------------------'''
'''----------------       sensor_task     -------------------'''
def sensor_task(key,item,hdlDB):
  while True:
    data=None
    internalLogger.debug("Gathering data from sensor '{0}'".format(key))
    data = item['handler'].getData()
    # Insert in DB 
    if data is not None:
      hdlDB.addData(data);
    if item['devType'] == "BT":
      time.sleep(1) # rate will be really set from peer
    elif item['devType'] == "LOCAL":
      time.sleep(20) # rate will be set here


'''----------------------------------------------------------'''
'''----------------     parse_args        -------------------'''
def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='Sensor data collector')
    parser.add_argument('--dbhost', type=str, required=False,
                        default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--dbport', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    parser.add_argument("-l","--launchContainers", action="store_true",
                        help='launch influxdb and grafana containers at startup')

    return parser.parse_args()

'''----------------------------------------------------------'''
'''----------------    printPlatformInfo  -------------------'''
def printPlatformInfo():
    print("Running on OS '{0}' release '{1}' platform '{2}'.".format(os.name,platform.system(),platform.release()))
    print("Uname raw info: {0}".format(os.uname()))
    print("Arquitecture: {0}".format(os.uname()[4]))
    print("Python version: {0}".format(sys.version_info))

'''----------------------------------------------------------'''
'''----------------       '__main__'      -------------------'''
if __name__ == '__main__':
    printPlatformInfo()
    args = parse_args()
    main(host=args.dbhost, port=args.dbport,lc=args.launchContainers)
