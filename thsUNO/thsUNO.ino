#include <SoftwareSerial.h>
#include "thsem.h"
#include "ledem.h"

//-------- Global variables declarations -----------

// TH Sensor object
thsem mythSensor;
const int datapinDHT22 = 2;

// Led Pin 13 has an LED connected on most Arduino boards, for debugging.
const int datapinLED = 13;
ledem myLed;

// Misc counter
int aliveLoopCounter=0;

//--------- Global functions declarations ------------



void(* resetFunc) (void) = 0;//declare reset function at address 0

//-------------------------------------
//--------- SETUP FUNCTION ------------
//-------------------------------------
void setup() { 

  // Serial to debug               
  Serial.begin(9600);
  Serial.println("Setup...");
 
  // LED to debug
  myLed.setup(datapinLED);
  myLed.hello();

  Serial.println("Setup...");
  if (mythSensor.setup(datapinDHT22)!=0) {
    Serial.print("Failing dht22 setup on pin:");
    Serial.println(datapinDHT22);
    Serial.print("Reset in a few seconds...");
    delay(5);
    resetFunc(); //call reset  
  }
 

  Serial.println("Setup DONE");
}

//-------------------------------------
//--------- LOOP  FUNCTION ------------
//-------------------------------------
void loop() {

   myLed.alive();

   if (mythSensor.refresh()!=0){
     Serial.println("Error reading DHT sensor¡¡¡");
     //TODO if problem persists in N loops maybe is worthy a reset?
   }
   else {
     Serial.print("Read data form DTH: Temperature:");
     Serial.print(mythSensor.getTemperature());
     Serial.print(" Celsius. Humidity(%):");
     Serial.println(mythSensor.getHumidity());
   }

   Serial.print(aliveLoopCounter++);
   Serial.println(" ... and still alive");

}


