#!/usr/bin/env python
import argparse
import time
import sys
import json
import subprocess
import os
import platform
import threading
import helper

from helper import *
from dbwrapper import *
from btwrapper import *
from localdhtwrapper import *

configuration={}

'''----------------------------------------------------------'''
'''----------------       M A I N         -------------------'''
'''----------------------------------------------------------'''

def main(host, port,lc,configfile):
  print('SCSEM-start -----------------------------')   

  # Loading config file,
  # Default values
  cfg_log_traces="scsem.log"
  cfg_log_exceptions="scseme.log"
  cfg_SensorsDirectory={}
  cfg_lc=lc
  cfg_database_dbhost=host
  cfg_database_dbport=port
  cfg_bt_enable=True
  cfg_bt_retryTimeSeconds=20
  # Let's fetch data
  with open(configfile) as json_data:
      configuration = json.load(json_data)
  #Get log names
  if "log" in configuration:
      if "logTraces" in configuration["log"]:
        cfg_log_traces = configuration["log"]["logTraces"]
      if "logExceptions" in configuration["log"]:
        cfg_log_exceptions = configuration["log"]["logExceptions"]
  helper.init(cfg_log_traces,cfg_log_exceptions)
  print('See logs traces in: {0} and exeptions in: {1}-----------'.format(cfg_log_traces,cfg_log_exceptions))  
  helper.internalLogger.critical('SCSEM-start -------------------------------')  
  helper.einternalLogger.critical('SCSEM-start -------------------------------')
  try:
    #Get sensors list
    cfg_SensorsDirectory = configuration["Sensors"]
    #Override args if available in config file
    if "launchContainers" in configuration:
      cfg_lc = configuration["launchContainers"]
    if "DataBase" in configuration:
      if "dbhost" in configuration["DataBase"]:
        cfg_database_host = configuration["DataBase"]["dbhost"]
      if "dbport" in configuration["DataBase"]:
        cfg_database_port = configuration["DataBase"]["dbport"]
    if "BluetoothSettings" in configuration:
      if "isBtEnabled" in configuration["BluetoothSettings"]:
        cfg_bt_enabled = configuration["BluetoothSettings"]["isBtEnabled"]
        if not cfg_bt_enabled:
          helper.internalLogger.warning("Bluetooth devices are not enabled this time in config.")
      if "retryTimeSeconds" in configuration["BluetoothSettings"]:
        cfg_bt_retryTimeSeconds = configuration["BluetoothSettings"]["retryTimeSeconds"]

  except Exception as e:
    helper.internalLogger.critical("Error processing configuration json {0} file. Exiting".format(configfile))
    helper.einternalLogger.exception(e)
    loggingEnd()
    return  

  if cfg_lc==True:
     launchContainers()

  try:    
    hdlDB=dbWrapper(cfg_database_host, cfg_database_port,
                    user = 'root',password = 'root',
                    dbname = 'db_emem',
                    dbuser = 'user_emem', dbpss = 'emem') 

    for key,item in cfg_SensorsDirectory.items():
      if item['devType'] == "BT":
           if not cfg_bt_enabled:
             helper.internalLogger.debug("Skipping creating BT object handler, bluethooth devices are disabled.")
             continue            
           helper.internalLogger.debug("Creating BT object handler...")
           x=btWrapper(key,item,speed=9600,timeout=cfg_bt_retryTimeSeconds)
           x.tryReconnect()
      elif item['devType'] == "LOCAL":
           helper.internalLogger.debug("Creating local DHT object handler...")
           x=localDhtWrapper(key,item)
      else:
           helper.internalLogger.error("Unknown sensor device type, ignoring it")
           continue
      item['handler']=x
      sensorTask=threading.Thread(target=sensor_task,args=(key,item,hdlDB,),name=key)
      sensorTask.daemon = True
      sensorTask.start()
      
    while True:
        time.sleep(1) 

  except Exception as e:
    e = sys.exc_info()[0]
    helper.internalLogger.critical('Error: Exception unprocessed properly. Exiting')
    helper.einternalLogger.exception(e)  
    print('SCSEM-General exeception captured. See ssms.log:{0}',format(cfg_log_exceptions))        
    loggingEnd()


'''----------------------------------------------------------'''
'''----------------       loggingEnd      -------------------'''
def loggingEnd():      
  helper.internalLogger.critical('SCSEM-end -----------------------------')        
  print('SCSEM-end -----------------------------')


'''----------------------------------------------------------'''
'''----------------       launchContainers-------------------'''
def launchContainers():
      try:
        helper.internalLogger.info("Relaunching containers...")
        p=subprocess.Popen([os.path.dirname(os.path.realpath(__file__))+'/launchContainers.sh','verbose'])      
        helper.internalLogger.debug("Script for launching container started  with popen:")
      except KeyboardInterrupt:
        print("Ok ok, quitting")
        sys.exit(1)
      except Exception as e:
        e = sys.exc_info()[0]
        helper.internalLogger.error('Unexpected error launching containers. Not recovery so far TODO.')
        helper.einternalLogger.exception(e)  
        time.sleep(5)
        sys.exit(1)
'''----------------------------------------------------------'''
'''----------------       sensor_task     -------------------'''
def sensor_task(key,item,hdlDB):
  while True:
    data=None
    helper.internalLogger.debug("Gathering data from sensor '{0}'".format(key))
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
    parser.add_argument('--configfile', type=str, required=False,
                        default='/etc/emem/scsem.conf',
                        help='Config file for scsem emem service')
    parser.add_argument('--dbhost', type=str, required=False,
                        default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--dbport', type=int, required=False, 
                        default=8086,
                        help='port of InfluxDB http API')
    parser.add_argument("-l","--launchContainers", 
                        action="store_true",
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
    main(host=args.dbhost, port=args.dbport,lc=args.launchContainers,configfile=args.configfile)
