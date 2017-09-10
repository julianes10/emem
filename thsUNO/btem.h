#ifndef BTEM_h
#define BTEM_h

#include "Arduino.h"
#include <SoftwareSerial.h>
#include "btem.h"


class btem
{
 public:

  btem();
  int setup(unsigned int v,unsigned int rx,unsigned int tx);
  int send(char *text);
  int send(unsigned int id,float t,float h);
  int sendKO(unsigned int id);
  void refresh();
  void powerOn();
  void powerOff();

 private:
  SoftwareSerial *bt;
  unsigned int vcc;
 
};

#endif


