#include "thingProperties.h"
const int trigger = 4; // Pin connected to the trigger pin of the sensor
const int echo = 2;    // Pin connected to the echo pin of the sensor


void setup() {
  // Initialize serial and wait for port to open:
  Serial.begin(9600);
  // This delay gives the chance to wait for a Serial Monitor without blocking if none is found
  delay(1500); 

  // Defined in thingProperties.h
  initProperties();

  // Connect to Arduino IoT Cloud
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);
  
  /*
     The following function allows you to obtain more information
     related to the state of network and IoT Cloud connection and errors
     the higher number the more granular information you’ll get.
     The default is 0 (only errors).
     Maximum is 4
 */
  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();

    // Set the trigger pin as an output
  pinMode(trigger, OUTPUT);
  // Set the echo pin as an input
  pinMode(echo, INPUT);
}

int getUltrasonicDistance(){
  // Function to retreive the distance reading of the ultrasonic sensor
  long duration;
  int weenoDistance;

  // Assure the trigger pin is LOW:
  digitalWrite(trigger, LOW);
  // Brief pause:
  delayMicroseconds(5);

  // Trigger the sensor by setting the trigger to HIGH:
  digitalWrite(trigger, HIGH);
  // Wait a moment before turning off the trigger:
  delayMicroseconds(10);
  // Turn off the trigger:
  digitalWrite(trigger, LOW);

  // Read the echo pin:
  duration = pulseIn(echo, HIGH);
  // Calculate the distance in centimeter (CM):
  weenoDistance = duration * 0.034 / 2;

  // Uncomment this line to return value in IN instead of CM:
  //distance = distance * 0.3937008

  // Return the distance read from the sensor:
  return weenoDistance;
}

void loop() {
  ArduinoCloud.update();
  // Your code here 
  weenoDistance = getUltrasonicDistance();
  Serial.println("Distance: " + String(weenoDistance));
  delay(1000);
}

/*
  Since distance is READ_WRITE variable, onWeenoDistance() is
  executed every time a new value is received from IoT Cloud.
*/
void onWeenoDistanceChange()  {
  // Add your code here to act upon distance change
  Serial.println("--onWeenoDistanceChange");
}