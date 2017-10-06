#!/usr/bin/env python
import sys
import os
import helper
'''----------------------------------------------------------'''
'''---------------- class bluethoot dht22 wrapper------------'''
class localDhtWrapper:

    def __init__(self,key,d):
      self.gpio=d['gpio']
      self.name2db=key
   
    def getData(self):
      if not helper.amIaPi():
        helper.internalLogger.info("No arm (pi) architecture detected. Ignoring sensor")
        return None
      
      import Adafruit_DHT
      
      helper.internalLogger.debug("Getting data from local dht22 on pin {0}...".format(self.gpio))
      humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, self.gpio)
      data=None
      if humidity is not None and temperature is not None:
        helper.internalLogger.info("Sensor '{0}' OK Temperature:{1}".format(self.name2db,temperature))
        data= [{
              "measurement": "temperature",
              "tags": {
                  "sensor": self.name2db,
              },
              "fields": {
                  "value": float(temperature),
              }},
              {
              "measurement": "humidity",
              "tags": {
                  "sensor": self.name2db,
              },
              "fields": {
                  "value": float(humidity),
              }}] 
      else:
        helper.internalLogger.debug("No data available on local dht22..:")

      return data


