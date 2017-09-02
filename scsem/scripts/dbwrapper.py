#!/usr/bin/env python
from influxdb import InfluxDBClient
import sys
import os
from collectorCommon import *
'''----------------------------------------------------------'''
'''---------------- class database wrapper       ------------'''

class dbWrapper ():

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
      internalLogger.info("Try reconnection to database" + self.dbname)
      try:
        """Instantiate a connection to the InfluxDB."""
        self.client = InfluxDBClient(self.host, self.port, self.user, self.password,self.dbname)

        internalLogger.info("Create database: " + self.dbname)
        self.client.create_database(self.dbname)

        internalLogger.info("Create a retention policy")
        self.client.create_retention_policy('awesome_policy', '3d', 3,default=True)

        internalLogger.info("Switch user: " + self.dbuser)
        self.client.switch_user(self.dbuser, self.dbpss)
      except KeyboardInterrupt:
          print("Ok ok, quitting")
          sys.exit(1)
      except Exception as e:
          e = sys.exc_info()[0]
          internalLogger.error('Unexpected error attempting to access to BD. It will be retried later.')
          einternalLogger.exception(e)  

    def addData(self, data):
        try: 
          json_body = data
          self.client.write_points(json_body)
        except KeyboardInterrupt:
            print("Ok ok, quitting")
            sys.exit(1)
        except Exception as e:
            e = sys.exc_info()[0]
            internalLogger.error('Unexpected error inserting in DB')
            einternalLogger.exception(e)  
            self.tryReconnect()
