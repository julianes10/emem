#include <SoftwareSerial.h>
#include "LowPower.h"
#include "thsem.h"
#include "btem.h"

//-------- Global variables declarations -----------

// TH Sensor object
#define MAX_SENSORS 2
thsem mythSensor[MAX_SENSORS];
int datapinDHT22[MAX_SENSORS]={2,5};

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
  for (int i=0;i<MAX_SENSORS;i++)
  {
    Serial.print("Setup DHT22 ");
    Serial.print(i+1);
    Serial.println(" ...");
    if (mythSensor[i].setup(datapinDHT22[i])!=0) {
      Serial.print("Failing dht22 setup on pin:");
      Serial.println(datapinDHT22[i]);
      Serial.print("Reset in a few seconds...");
      delay(5);
      resetFunc(); //call reset  
    }
  }
  
  Serial.println("Setup BT HC05...");
  if (myBT.setup(datapinRxBT,datapinTxBT,10)!=0) {
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
 int newTimer=0;  
 
 if (1)//TEST aliveLoopCounter%8 == 0)
 {
   //Sending data 1 every minute more or less
   for (int i=0;i<MAX_SENSORS;i++)
   {
     if (mythSensor[i].refresh()!=0){
       Serial.println("Error reading DHT sensor");
       //TODO if problem persists in N loops maybe is worthy a reset?
       newTimer=myBT.sendKO(i+1);
       Serial.print("New timer received:");
       Serial.println(newTimer);
     }
     else {
       float t=mythSensor[i].getTemperature();
       float h=mythSensor[i].getHumidity();
       Serial.print("Read data from ");
       Serial.print(i+1);
       Serial.print(" DTH: Temperature:");
       Serial.print(t);
       Serial.print(" Celsius. Humidity(%):");
       Serial.println(h);
       newTimer=myBT.sendWaitNewPeriod(i+1,t,h);
       //myBT.send(i+1,t,h);
       Serial.print("New timer received:");
       Serial.println(newTimer);
     }
   }
 }
/*TODO       if (newTimer<=0) {
         //TODO if problem persists in N loops maybe is worthy a reset?
      }
*/
 Serial.print(aliveLoopCounter++);
 Serial.println(" ... and still alive, let's power done 8 secs..");
delay(5000);//TEST LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);

}


