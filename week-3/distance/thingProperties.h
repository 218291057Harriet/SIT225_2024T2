#include <ArduinoIoTCloud.h>  // LIBRARY NEEDS TO BE INSTALLED
#include <Arduino_ConnectionHandler.h>  // LIBRARY NEEDS TO BE INSTALLED
#include <ArduinoHttpClient.h>
#include "arduino_secrets.h"

const char SSID[]     = SECRET_SSID;    // Network SSID (name)
const char PASS[]     = SECRET_OPTIONAL_PASS;    // Network password (use for WPA, or use as key for WEP)

void onWeenoDistanceChange();

int weenoDistance;

void initProperties(){
  ArduinoCloud.addProperty(weenoDistance, READWRITE, ON_CHANGE, onWeenoDistanceChange);
}

WiFiConnectionHandler ArduinoIoTPreferredConnection(SSID, PASS);