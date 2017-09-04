#include <Arduino.h>
#include <SoftwareSerial.h>
#include "btem.h"



btem::btem()
{

}

int btem::setup(unsigned int rx,unsigned int tx)
{
  bt=new SoftwareSerial(10, 11);
  bt->begin(9600);
  if (bt!=0) return 0;
  return 1;
}
int btem::send(char *text) {
  bt->println(text);
return 0;
}

int btem::send(unsigned int id,float t,float h) {
  bt->print("{\"id\":\"id");
  bt->print(id);
  bt->print("\",\"status\":\"");
  bt->print("OK");
  bt->print("\",\"data\":{\"t\":\"");
  bt->print(t);
  bt->print("\",\"h\":\"");
  bt->print(h);
  bt->println("\"}}");

  //TODO WAIT FOR ACK UNTIL A TIMEOUT
return 0; //TODO
}

int btem::sendKO(unsigned int id) {
  bt->print("{\"id\":\"id");
  bt->print(id);
  bt->print("\",\"status\":\"");
  bt->print("KO");
  bt->println("\"}");
return 0; //TODO
}

void btem::refresh() {  
}




