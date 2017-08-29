#ifndef BTEM_h
#define BTEM_h

#include "Arduino.h"
#include <SoftwareSerial.h>
#include "btem.h"


class btem
{
 public:

  btem();
  int setup(unsigned int rx,unsigned int tx);
  int send(char *text);
  int send(float t,float h);
  int sendKO();
  void refresh();

 private:
  SoftwareSerial *bt;
};

#endif

