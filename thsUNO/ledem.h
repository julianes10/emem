#ifndef LEDEM_h
#define LEDEM_h

#include "Arduino.h"
#include "ledem.h"


class ledem
{
 public:

  ledem();
  void setup(unsigned int datapin);
  void hello();
  void alive();

 private:
  int led; 
};

#endif


