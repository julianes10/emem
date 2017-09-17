#include <Arduino.h>

#include "ledem.h"

ledem::ledem()
{
 led=0;
}

void ledem::setup(unsigned int datapin)
{
  pinMode(datapin, OUTPUT);
  led=datapin;
}
void ledem::hello() {
  for (int i=0;i<1;i++){
   digitalWrite(led, HIGH);  
   delay(250);               
   digitalWrite(led, LOW);  
   delay(250);  
  }
}

void ledem::alive() {
  for (int i=0;i<2;i++){
   digitalWrite(led, HIGH);  
   delay(100);               
   digitalWrite(led, LOW);    
   delay(200); 
  }
}
