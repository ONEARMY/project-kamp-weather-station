#include "configReader.h"

SDFile configFile;        // Create configFile instance from the SD library

bool readSetting(char *fileContent, int contentLength, const char *settingName, char *returnBuff, int returnLength) {
   // strncpy(buf, key, l);
   char ContentBuf[contentLength];
  strncpy(ContentBuf, fileContent, sizeof(ContentBuf));
  char *saveptr1;
  char *saveptr2;

  // loop over \n tokens
  char *tok1 = strtok_r(ContentBuf, "\n", &saveptr1);
  while (tok1 != NULL) {
    // loop over = token
    char *tok2 = strtok_r(tok1, "=", &saveptr2);
    if (tok2 != NULL) {
       if (strcmp(tok2, settingName) == 0) {
           tok2 = strtok_r(NULL, "=", &saveptr2);
           if (tok2 != NULL) {
             strncpy(returnBuff, tok2, returnLength - 1);
           }
           return 0;
       }
    }

    tok1 = strtok_r(NULL, "\n", &saveptr1);
  }
      return true;
}

bool readFileContents(const char *fileName, char *content, int length) {
  if (!SD.begin(4)) {
    Serial.println(F("INITIALIZING SD CARD FAILED"));
    return false;
  }
  else {
    //Serial.println("INITIALIZING SD CARD COMPLETED");
    //Serial.println("OPENING FILE: " + String(fileName));
    configFile = SD.open(fileName);
    if (!configFile) {
      //Serial.println("ERROR OPENING FILE: " + String(fileName));
      return false;
    }
    else {
      int i = 0;
      char c;
      while (configFile.available()) {
        c = configFile.read();
        if (i < (length - 1)) {
          content[i] = c;
          i++;
        }
      }
      configFile.close();
      return true;
    }
  }
}