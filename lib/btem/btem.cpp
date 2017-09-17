#include <Arduino.h>
#include <SoftwareSerial.h>
#include "btem.h"



btem::btem()
{
  vcc=-1;
}

int btem::setup(unsigned int v,unsigned int rx,unsigned int tx, unsigned int toutsec)
{
  vcc=v;
  pinMode(vcc, OUTPUT); 
  powerOn();
  return this->setup(rx,tx,toutsec);
}

int btem::setup(unsigned int rx,unsigned int tx, unsigned int toutsec)
{
  // WORKING bt=new SoftwareSerial(10, 11);
  // NOTE Rx pin bt is my arduino serial TX
  // NOTE Tx pin bt is my arduino serial RX
  bt=new SoftwareSerial(tx, rx); // SoftwareSerial(rxPin, txPin, inverse_logic)
  bt->begin(9600);
  bt->setTimeout(toutsec*1000);
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

return 0; //TODO
}

int btem::sendWaitNewPeriod(unsigned int id,float t,float h) {
  String s="";
  this->send(id,t,h);
  s=bt->readString();
  
return s.toInt(); 
}

int btem::sendKO(unsigned int id) {    
  String s="";
  bt->print("{\"id\":\"id");
  bt->print(id);
  bt->print("\",\"status\":\"");
  bt->print("KO");
  bt->println("\"}");
  s=bt->readString();
  return s.toInt();
}

void btem::powerOn()
{
  if (this->vcc >= 0) {
    digitalWrite(vcc,HIGH);
    delay(5000);
  }
}

void btem::powerOff()
{
  if (this->vcc >= 0) {
    delay (5000);
    digitalWrite(vcc,LOW);
  }
}

void btem::refresh() {  
}




