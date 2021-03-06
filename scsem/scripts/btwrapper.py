#!/usr/bin/env python
import sys
import json
import subprocess
import os
import time
import serial
import helper
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
        helper.internalLogger.info("Try to reconnect btmac: {0} to port: {1}".format(self.mac,self.port))
        aux=subprocess.check_output([EMEM_DEPLOY_DIR+'/scsem/scripts/bindBTmac.sh',self.mac,self.port,'verbose'])      
        helper.internalLogger.debug("Bind script output:" + aux)    
      except subprocess.CalledProcessError as e:
        helper.internalLogger.debug("Bind script return error {0} {1}.".format(e.returncode, e.message))
        return False
      except KeyboardInterrupt:
        print("Ok ok, quitting")
        sys.exit(1)
      except Exception as e:
        e = sys.exc_info()[0]
        helper.internalLogger.error('Unexpected error binding to btmac. It will be retried later.')
        helper.einternalLogger.exception(e)  
        return False
      helper.internalLogger.info("Device visible {0} now trying setup serial interface towards it...".format(self.mac))
      try:
        helper.internalLogger.info("Try open serial port:" + self.port)
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
        helper.internalLogger.error('Unexpected error accesing to serial port. It will be retried later.')
        helper.einternalLogger.exception(e)  
        self.ser=None
        return False
      return True


    def getData(self):
      helper.internalLogger.debug("Getting data from bt {0}...".format(self.port))
      #Check ser status
      if self.ser==None:
        if self.tryReconnect():
           helper.internalLogger.error('Serial line ready to be read.')
        else:
           helper.internalLogger.error('Serial line is not seem to be read.') 
           time.sleep(10)
           return None;
          
      line=None     
      data=None
      i=0
      while True:
        try:
          line = self.ser.readline()
        except KeyboardInterrupt:
          print("Ok ok, quitting")
          sys.exit(1)
        except Exception as e:
          e = sys.exc_info()[0]
          helper.internalLogger.error('Unexpected error reading line from remote serial bt device.')
          helper.einternalLogger.exception(e)
          self.ser=None
          return data
        helper.internalLogger.debug("Got line, cool")                  
        if line is not None: 
            try:
              helper.internalLogger.debug("Something read yeah...:" + line)
              json_acceptable_string = line.replace("'", "\"")
              d = json.loads(json_acceptable_string)
              # One line per dht
              if d['status'] == "OK":
                id2use=self.name2db
                helper.internalLogger.info("Sensor '{0}'-'{1}' OK Temperature:{2}".format(self.name2db,d['id'],d['data']['t']))
                if self.subnames != None:
                  #Check id's are expected ones
                  if not d['id'] in self.subnames:
                    helper.internalLogger.critical("Unrecognized id: {0}. Expected: {1}. Discarded".format(d['id'],self.subnames))
                    continue
                  else:
                    id2use= self.subnames[d['id']]
                data= [
                      {"measurement": "temperature","tags": {"sensor": id2use},"fields": {"value": float(d['data']['t'])}},
                      {"measurement": "humidity",   "tags": {"sensor": id2use},"fields": {"value": float(d['data']['h'])}}]
                self.ser.write("30\n")
                self.ser.flush()
                return data
              else:
                helper.internalLogger.debug("Sensor KO")
                self.ser.write("20\n")
                self.ser.flush()
                continue
            except Exception as e:
              helper.internalLogger.debug("Error processing line as json, ignoring it")
              e = sys.exc_info()[0]
              helper.einternalLogger.exception(e)  
        else:
            helper.internalLogger.debug("No data available on serial BT yet...:")

      

