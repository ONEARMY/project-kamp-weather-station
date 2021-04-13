#include <configReader.h>

void setup()
{
  Serial.begin(9600);
  pinMode(4, OUTPUT);		//Set the Chip Select pin as an output
  char ssid[20];			//Create a char arrey to store the SSID
  char pswd[30];			//Create a char arrey to store the PSWD
  char filecontents[200];	//Create a buffer for the file contents
  //Set the buffers to all 0
  memset(filecontents, 0, sizeof(filecontents));
  memset(ssid, 0, sizeof(ssid));
  memset(pswd, 0, sizeof(pswd));
  //read the file contents of config.txt and write it to the filecontents buffer
  readFileContents("config.txt", filecontents, sizeof(filecontents));
  //read the buffer and search for the config identifier SSID / PSWD
  readSetting(filecontents, sizeof(filecontents), "SSID", ssid, sizeof(ssid));
  readSetting(filecontents, sizeof(filecontents), "PSWD", pswd, sizeof(pswd));
  Serial.println("Connecting to WiFi");
  //connect to wifi (ESP8266 or ESP32)
  connectWifi(ssid, pswd);
}

void loop() {
    
}