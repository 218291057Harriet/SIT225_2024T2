/*
    Harriet Rawson
    s218291057
*/

int x;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);  // Set baud rate

}

void loop() {
  while (!Serial.available()) {} 

  // Read string sent by Python to integer.
  x = Serial.readString().toInt();

  // Peform blink as many times as given integer.
  for (int i = 0; i < x; i++)
  {
    digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)
    delay(1000);                      // wait for a 1 second
    digitalWrite(LED_BUILTIN, LOW);   // turn the LED off by making the voltage LOW
    delay(1000);                      // wait for a second
  }

  // Sending back a random integer for sleepy time
  int response = random(1, 10);
 

  // Write integer sent to Python
  Serial.println(response);  

  // Push the data through serial channel.
  Serial.flush();  
}