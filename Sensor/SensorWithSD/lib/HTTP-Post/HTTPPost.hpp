#ifndef __HTTPPOST_H__
#define __HTTPPOST_H__

#include <Arduino.h>

void emptyESP_RX(unsigned long duration);
bool waitForString(const char * endMarker, unsigned long duration);
bool espATCommand(const char * command, const char * endMarker, unsigned long duration);
void resetESP();
bool connectWifi(const char *ssid, const char *pswd);
void append(char *s, char c);
void httpPost(const char *serverIP, const char *serverURI, char *httpRequest);
#endif