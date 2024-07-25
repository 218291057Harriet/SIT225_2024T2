/*
    Harriet Rawson
    s218291057
*/

#include <DHT.h>

#define DHTPIN 2  // digital pin number
#define DHTTYPE DHT22  
DHT dht(DHTPIN, DHTTYPE);

// Variables to store data.
float hum, temp;

void setup() {
  // Set baud rate for serial communication
  Serial.begin(9600);

  // Initialise DHT libarary
  dht.begin();
}

void loop() {
  // Read data
  hum = dht.readHumidity();
  temp = dht.readTemperature();

  // Print data to the serial port
  Serial.print(hum);
  Serial.print(",");
  Serial.println(temp);


  // Wait 30 seconds before looping
  delay(30000);
}