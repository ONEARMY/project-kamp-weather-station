#include "main.h"

char *httpRequestData; // The request will be build in this String

char ip[16];
char URI[20];
char apikey[20];

//Converts the input and a type (temp, humidity, windspeed, wind direction) to a readable value for the database
float converter(uint8_t channel, uint8_t type)
{
  if (type == 0) {

  }
  else if (type == 1) {

  }
}

void setup()
{
  // put your setup code here, to run once:
  Serial1.begin(115200); while(!Serial1);
  Serial.begin(9600);
  pinMode(4, OUTPUT);
  char ssid[20];
  char pswd[30];
  char filecontents[200];
  memset(filecontents, 0, sizeof(filecontents));
  memset(ssid, 0, sizeof(ssid));
  memset(pswd, 0, sizeof(pswd));
  memset(ip, 0, sizeof(ip));
  memset(URI, 0, sizeof(URI));
  _delay_ms(1000);
  readFileContents("config.txt", filecontents, sizeof(filecontents));
  readSetting(filecontents, sizeof(filecontents), "SSID", ssid, sizeof(ssid));
  readSetting(filecontents, sizeof(filecontents), "PSWD", pswd, sizeof(pswd));
  readSetting(filecontents, sizeof(filecontents), "IP", ip, sizeof(ip));
  readSetting(filecontents, sizeof(filecontents), "POST", URI, sizeof(URI));
  readSetting(filecontents, sizeof(filecontents), "APIKey", apikey, sizeof(apikey));
  Serial.println(F("Connecting to WiFi"));
  resetESP();
  connectWifi(ssid, pswd);
}
 
void loop()
{
  // put your main code here, to run repeatedly:
  unsigned long timeBefore = millis();
  unsigned char Temp = converter(A0, 0);
  Serial.print(F("Sensor: "));
  Serial.println(Temp);
  sprintf(httpRequestData, "api_key=%s&temp=%i", apikey, Temp);

  httpPost(ip, URI, httpRequestData);
  while (millis() <= (timeBefore + 60000))
  {
    _delay_ms(1);
  }
}