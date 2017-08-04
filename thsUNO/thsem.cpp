#include <Arduino.h>

#include "thsem.h"

thsem::thsem()
{
  dht=0;
  t=0;
  h=0;
}

int thsem::setup(unsigned int datapin)
{
  dht=new DHT(datapin, DHT22); //// Initialize DHT sensor for normal 16mhz Arduino
  if (dht)
    dht->begin();
  else
    return -1;
  return 0;
}
int thsem::refresh()
{
  //Read data and store it to variables hum and temp
  h = dht->readHumidity();
  t = dht->readTemperature();
  return 0;
}




