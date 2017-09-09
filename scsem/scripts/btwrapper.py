#!/usr/bin/env python
import sys
import json
import subprocess
import os
import time
import serial
from collectorCommon import *
'''----------------------------------------------------------'''
'''---------------- class bluethoot dht22 wrapper------------'''

class btWrapper():

    def __init__(self,key,d,speed,timeout):
      self.port=d['port']
      self.speed=speed
      self.timeout=timeout
      self.ser=None
      self.mac=d['btmac']
      self.subnames=None
      if 'subnames' in d:
        self.subnames=d['subnames']
      self.name2db=key

    def tryReconnect(self):
      self.ser=None
      try:
        internalLogger.info("Try to reconnect btmac: {0} to port: {1}".format(self.mac,self.port))
        aux=subprocess.check_output([EMEM_DEPLOY_DIR+'/scsem/scripts/bindBTmac.sh',self.mac,'verbose'])      
        internalLogger.debug("Bind script output:" + aux)    
      except subprocess.CalledProcessError as e:
        internalLogger.debug("Bind script return error {0} {1}.".format(e.returncode, e.message))
        return False
      except KeyboardInterrupt:
        print("Ok ok, quitting")
        sys.exit(1)
      except Exception as e:
        e = sys.exc_info()[0]
        internalLogger.error('Unexpected error binding to btmac. It will be retried later.')
        einternalLogger.exception(e)  
        return False
      internalLogger.info("Device visible {0} now trying setup serial interface towards it...".format(self.mac))
      try:
        internalLogger.info("Try open serial port:" + self.port)
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
      except Exception as e:
        e = sys.exc_info()[0]
        internalLogger.error('Unexpected error accesing to serial port. It will be retried later.')
        einternalLogger.exception(e)  
        self.ser=None
        return False
      return True


    def getData(self):
      internalLogger.debug("Getting data from bt {0}...".format(self.port))
      #Check ser status
      if self.ser==None:
        if self.tryReconnect():
           internalLogger.error('Serial line ready to be read.')
        else:
           internalLogger.error('Serial line is not seem to be read.') 
           time.sleep(60)
           return None;
          
      line=None     
      data=None
      i=0
      while line==None and i<2:
        i=i+1
        try:
          line = self.ser.readline()
          internalLogger.debug("Got line, cool")
          break
        except KeyboardInterrupt:
          print("Ok ok, quitting")
          sys.exit(1)
        except Exception as e:
          e = sys.exc_info()[0]
          internalLogger.error('Unexpected error reading line from remote serial bt device. Trying to reconnect')
          einternalLogger.exception(e)  
          self.tryReconnect()

      internalLogger.debug("Checking line value...")
      if line is not None: 
        try:
          internalLogger.debug("Something read yeah...:" + line)
          json_acceptable_string = line.replace("'", "\"")
          d = json.loads(json_acceptable_string)
          #One line per dht

          if d['status'] == "OK":
            id2use=self.name2db
            internalLogger.info("Sensor '{0}'-'{1}' OK Temperature:{2}".format(self.name2db,d['id'],d['data']['t']))
            if self.subnames != None:
              #Check id's are expected ones
              if not d['id'] in self.subnames:
                internalLogger.critical("Unrecognized id: {0}. Expected: {1}. Discarded".format(d['id'],self.subnames))
                return None
              else:
                id2use= self.subnames[d['id']]
            data= [{
              "measurement": "temperature",
              "tags": {
                  "sensor": id2use,
              },
              "fields": {
                  "value": float(d['data']['t']),
              }},
              {
              "measurement": "humidity",
              "tags": {
                  "sensor": id2use,
              },
              "fields": {
                  "value": float(d['data']['h']),
              }}] 
          else:
            internalLogger.debug("Sensor KO")          
        except Exception as e:
          internalLogger.debug("Error processing line as json, ignoring it")
          e = sys.exc_info()[0]
          einternalLogger.exception(e)  
      else:
        internalLogger.debug("No data available on serial BT...:")

      return data

