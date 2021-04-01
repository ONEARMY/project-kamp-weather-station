#include "HTTPPost.h"

const char *OK_STR = "OK\r\n";

char *response;        // The server response will be stored in this String

const int timeout = 5100; // Max timeout delay

/* 
 *  =====================================================================================
 *  --------------------------------------
 *   emptyESP_RX waits for duration ms
 *   and get rid of anything arriving
 *   on the ESP Serial port during that delay
 *   --------------------------------------
 */

void emptyESP_RX(unsigned long duration)
{
  unsigned long currentTime;
  currentTime = millis();
  while (millis() - currentTime <= duration)
  {
    if (Serial1.available() > 0)
      Serial1.read();
  }
}

/* 
 *  --------------------------------------
 *  waitForString wait max for duration ms
 *  while checking if endMarker string is received
 *  on the ESP Serial port
 *  returns a boolean stating if the marker
 *  was found
 *  --------------------------------------
 */

boolean waitForString(const char *endMarker, unsigned long duration)
{
  int localBufferSize = strlen(endMarker); // we won't need an \0 at the end
  char localBuffer[localBufferSize];
  int index = 0;
  boolean endMarkerFound = false;
  unsigned long currentTime;

  memset(localBuffer, '\0', localBufferSize); // clear buffer

  currentTime = millis();
  while (millis() - currentTime <= duration)
  {
    if (Serial1.available() > 0)
    {
      if (index == localBufferSize)
        index = 0;
      localBuffer[index] = (uint8_t)Serial1.read();
      endMarkerFound = true;
      for (int i = 0; i < localBufferSize; i++)
      {
        if (localBuffer[(index + 1 + i) % localBufferSize] != endMarker[i])
        {
          endMarkerFound = false;
          break;
        }
      }
      index++;
    }
    if (endMarkerFound)
      break;
  }
  return endMarkerFound;
}

/* --------------------------------------
 * espATCommand executes an AT commmand
 * checks if endMarker string is received
 * on the ESP Serial port for max duration ms
 * returns a boolean stating if the marker
 * was found
 *  --------------------------------------
 */

bool espATCommand(const char *command, const char *endMarker, unsigned long duration)
{
  Serial1.println(command);
  return waitForString(endMarker, duration);
}

void resetESP()
{
  espATCommand("AT+RST", OK_STR, 30);
  espATCommand("AT+CWMODE_DEF=1", OK_STR, 30);
  espATCommand("AT+CWDHCP_CUR=1,1", OK_STR, 30);
}

bool connectWifi(const char *ssid, const char *pswd)
{
  while (!Serial1);
  char *cmd;
  sprintf(cmd, "AT+CWJAP_DEF=\"%s\",\"%s\"", ssid, pswd);
  Serial1.println(cmd);
  Serial.println("Connecting");
  while (!(Serial1.find("WIFI")))
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" >> Connected!");
  return 0;
}

void append(char *s, char c)
{
  int len = strlen(s);
  s[len] = c;
  s[len + 1] = '\0';
}

void httpPost(const char *serverIP, const char *serverURI, char *httpRequest)
{
  char *CIPSTART;
  sprintf(CIPSTART, "AT+CIPSTART=\"TCP\",\"%s\",80", serverIP);
  Serial1.println(CIPSTART); // Tell the ESP01 to start a TCP connection.
  waitForString(OK_STR, 100);
  char *postRequest;
  sprintf(postRequest, "POST %s HTTP/1.1\r\nHost: %s\r\nAccept: */*\r\nContent-Length: %i\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\n", serverURI, serverIP, (char *)strlen(httpRequest));
  /*"POST "+ serverURI + " HTTP/1.1\r\n" + "Host: " + serverIP + "\r\n" +
    "Accept: *" + "/" + "*\r\n" + "Content-Length: " + httpRequest.length() + "\r\n" +
    "Content-Type: application/x-www-form-urlencoded\r\n" + "\r\n";
  */
  const char *sendCmd = "AT+CIPSEND="; //determine the number of caracters to be sent.
  int dataLengte = ((unsigned)strlen(postRequest) + (unsigned)strlen(httpRequest));
  // total datalength postrequest + Json string
  Serial1.println(dataLengte); // to ESP01
  Serial.print(sendCmd);
  Serial.println(dataLengte);
  delay(4000);
  // visualize on serial monitor
  if (Serial1.find(">"))
  { //wachten op > teken om de http header te kunnen versturen!!
    Serial.print(F("Sending.."));
    // to serial monitor
    Serial1.print(postRequest);
    Serial1.print(httpRequest); // to ESP01
    // to ESP01
    Serial.println(postRequest);
    Serial.println(httpRequest); // to serial monitor
    // to serial monitor
    if (Serial1.find("SEND OK"))
    {
      Serial.println(F("Packet sent"));
      long int time = millis(); // huidige klokwaarde opslaan in var time
      memset(response, 0, sizeof(response));            //response string leeg maken
      bool test = 0;
      while ((time + timeout) > millis())
      { // wachten zolang we niet over timeout waarde gaan
        while (Serial1.available())
        { // zolang er nieuwe data binnenkomt
          char c = Serial1.read();
          // read the next character.
          Serial.print(c);
          //1e maal dat ontvangen datastring wordt afgedrukt via serial monitor
          if (c == '{' or test == 1)
          {                      // vanaf het moment je een "{" tegenkomt , alle tekens voordien worden weggegooid, maar wel getoond op de serial monitor
            append(response, c); //voeg het laatst uitgelezen karakter toe aan de response string
            test = 1;
          }
        }
      }
      if (strlen(response) < 10)
        Serial.println("timeout"); // als de response <10 karakters bevat : response weggooien
      else
      {
        Serial.print("Data:");
        // to serial monitor
        Serial.println(response); //2e maal dat ontvangen datastring wordt afgedrukt via serial monitor
      }
      // close the connection
      Serial1.println("AT+CIPCLOSE");
      if (Serial1.find("OK"))
      { // wanneer ESP anwtoord met OK
        Serial.println("TCP connection closed");
      }
      delay(1000);
    }
    else
    {
      Serial.println("ERROR");
    }
  }
  else if (Serial1.find("ERROR"))
  {
    Serial.println("Fout: error gevonden");
  }
}