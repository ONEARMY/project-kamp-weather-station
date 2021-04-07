#ifndef __CONFIGREADER_H__
#define __CONFIGREADER_H__

#include <Arduino.h>
#include <SD.h>

bool readSetting(char *fileContent, int contentLength, const char *settingName, char *returnBuff, int returnLength);
bool readFileContents(const char *fileName, char *content, int length);

#endif