#ifndef THSEM_h
#define THSEM_h

#include "Arduino.h"
#include "thsem.h"
#include <Adafruit_Sensor.h>
#include <DHT.h>


class thsem
{
 public:

  thsem();
  int setup(unsigned int datapin);
  int refresh();
  float getTemperature(){return t;}
  float getHumidity(){return h;}

 private:
 DHT *dht; 
 float t;
 float h;
};

#endif


