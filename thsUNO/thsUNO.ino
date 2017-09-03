#include <SoftwareSerial.h>
#include "LowPower.h"
#include "thsem.h"
#include "ledem.h"
//#include "displayem.h"
#include "btem.h"

//-------- Global variables declarations -----------

// TH Sensor object
thsem mythSensor;
const int datapinDHT22 = 2;

// Led Pin 13 has an LED connected on most Arduino boards, for debugging.
const int datapinLED = 13;
ledem myLed;

// 128x32 display
//displayem myDisplay;


// Piezo buzzer
int piezoPin = 7;

// BT to report data
const int datapinRxBT = 10;
const int datapinTxBT = 11;
btem myBT;


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
  Serial.println("Setup... 'came on, be my baby, came on'");
 
  // Wake up buzzer
  Serial.println("Setup buzzer, hello...");
  tone(piezoPin, 1000, 500);

  // LED to debug
  Serial.println("Setup LED, hello...");
  myLed.setup(datapinLED);
  myLed.hello();


  Serial.println("Setup DHT22...");
  if (mythSensor.setup(datapinDHT22)!=0) {
    Serial.print("Failing dht22 setup on pin:");
    Serial.println(datapinDHT22);
    Serial.print("Reset in a few seconds...");
    delay(5);
    resetFunc(); //call reset  
  }

  
  Serial.println("Setup BT DHT22...");
  if (myBT.setup(datapinRxBT,datapinTxBT)!=0) {
    Serial.print("Failing BT setup on pins:RX:");
    Serial.print(datapinRxBT);
    Serial.print("-TX:");
    Serial.println(datapinTxBT);
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
     Serial.println("Error reading DHT sensor");
     myLed.hello();
     tone(piezoPin, 1000, 200);
     delay(500);
     tone(piezoPin, 1000, 200);
     //TODO if problem persists in N loops maybe is worthy a reset?
     myBT.sendKO();
   }
   else {
     float t=mythSensor.getTemperature();
     float h=mythSensor.getHumidity();
     Serial.print("Read data form DTH: Temperature:");
     Serial.print(t);
     Serial.print(" Celsius. Humidity(%):");
     Serial.println(h);
     if (myBT.send(t,h)!=0) {
       //TODO if problem persists in N loops maybe is worthy a reset?
       myLed.hello();
       tone(piezoPin, 2000, 1000);
     }
     else {
       myBT.send(t,h);
     }
   }

   Serial.print(aliveLoopCounter++);
   Serial.println(" ... and still alive, let's power done 8 secs..");
   LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF); 
}


