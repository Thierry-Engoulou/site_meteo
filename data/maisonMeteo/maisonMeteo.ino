 #include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <SPIFFS.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <ArduinoJson.h>
#include <Adafruit_BME280.h>
#include <LiquidCrystal_I2C.h>
//////////////////////////////////////////////////////////////
Adafruit_BME280 bme;
AsyncWebServer server(80); 
LiquidCrystal_I2C lcd(0x27, 16, 2); 

const char* ssid="SERRE";
const char* pass="123456789";
//////////////////////////////////////////////////


void writeToFile(String fichier, String donne) {
  File file = SPIFFS.open(fichier, FILE_APPEND);
  if (!file) {
    Serial.println("Failed to open file for writing");
    return;
  }
 file.println(donne);
  file.close();
}

void GlobalWriteToFile(String fichier, String donne1,String donne2,String donne3,String donne4,String donne5,String donne6) {
  File file = SPIFFS.open(fichier, FILE_APPEND);
  if (!file) {
    Serial.println("Failed to open file for writing");
    return;
  }
  String data= donne1 + " -----  " + donne2+ " -----  "+donne3+" -----  "+donne4+" -----  " + donne5+" -----  "+donne6;
 file.println(data);
  file.close();
}

String sortie(String fichier, int numLines) {
  File file = SPIFFS.open(fichier, FILE_READ);
  if (!file) {
    Serial.println("Failed to open file for reading");
    return "";
  }

  // Déterminer la taille du fichier
  file.seek(0, SeekEnd); // se position a la fin du fichier 
  int fileSize = file.position();

  // Trouver la position du début des 30 dernières lignes
  int position = fileSize;
  int linesRead = 0;
  while (position > 0 && linesRead < numLines) {
    position--;
    file.seek(position); // se position a la position n-1
    if (file.read() == '\n') {
      linesRead++;
    }
  }
  if (position > 0) {
    position++;
  }

  // Lire les 30 dernières lignes
  String lastLines = "";
  file.seek(position);
  while (file.position() < fileSize) {
    String line = file.readStringUntil('\n');
    if (lastLines.length() > 0) {
      lastLines += ",";
    }
    lastLines += line;
  }

  file.close();
  return lastLines;
}




///////////////////////////////////////

float temperature(){
   return bme.readTemperature();
}
float humidite(){
  return bme.readHumidity();
}
float pression(){
  return bme.readPressure() / 100.0F;
}

float UV(){
  return ((analogRead(34)* (3.3 / 4095.0))*10)/3.3;
}
float air(){
  return analogRead(25);
}
float vent(){
 return analogRead(27);
}
float volumePluie(){
  return (analogRead(2));
}

void afficheData(){
  lcd.setCursor(0,0);
  lcd.print("Pres:");
  lcd.setCursor(5,0);
  lcd.print(pression());
  lcd.setCursor(9,0);
  lcd.print("hum:");
  lcd.print(humidite());
  lcd.setCursor(0,1);
  lcd.print("UV:");
  lcd.setCursor(3,1);
  lcd.print(UV());
  lcd.setCursor(6,1);
  lcd.print("temp:");
  lcd.setCursor(12,1);
  lcd.print(temperature());
}



void setup() {
  Serial.begin(115200);
  ////////////////////////////////////////////////////////
  
  ////////////////////////////////////////////////////

  if (!bme.begin(0x76)) { 
    Serial.println("Erreur de connexion au capteur BME280 !");
    while (1);
  }

  ///////////////////////////////////////////////////////
  if (!SPIFFS.begin()) {
    Serial.println("Error SPIFFS....");
    return;
  }
  File root = SPIFFS.open("/");
  File file = root.openNextFile();
  while (file) {
    Serial.print("FILE: ");
    Serial.println(file.name());
    file.close();
    file = root.openNextFile();
  }



   WiFi.softAP(ssid,pass);
 Serial.print("Adresse IP");
 Serial.println(WiFi.softAPIP());
 lcd.init();
 lcd.backlight(); 
 lcd.setCursor(0, 0);
 lcd.setCursor(3,0);
 lcd.print("Welcome !!");
 delay(1500);
 lcd.clear();
 lcd.setCursor(0,0);
 lcd.print("Adress ip de l'esp32");
 lcd.setCursor(0,1);
 lcd.print(WiFi.localIP());
 delay(2000);

  ////////////////////////////////////////////////////////////////

  server.on("/", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    resquest->send(SPIFFS, "/index.html", "text/html");
  });
   server.on("/index.html", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    resquest->send(SPIFFS, "/index.html", "text/html");
  });
 
  server.on("/style.css", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    resquest->send(SPIFFS, "/style.css", "text/css");
  });
  server.on("/chart.js", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    resquest->send(SPIFFS, "/chart.js", "text/javascript");
  });
    server.on("/icon.png", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    resquest->send(SPIFFS, "/icon.png", "text/png");
  });
  server.on("/script.js", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    resquest->send(SPIFFS, "/script.js", "text/javascript");
  });
  server.on("/GlobalData.txt", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    resquest->send(SPIFFS, "/GlobalData.txt", "text/javascript");
  });

  ////////////////////////////////////////////////////////////////////////////

  server.on("/pression.html", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    resquest->send(SPIFFS, "/pression.html", "text/html");
  });
  server.on("/styleP.css", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    resquest->send(SPIFFS, "/styleP.css", "text/css");
  });
  server.on("/scriptP.js", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    resquest->send(SPIFFS, "/scriptP.js", "text/javascript");
  });
  server.on("/dataPress.txt", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    resquest->send(SPIFFS, "/dataPress.txt", "text/javascript");
  });

server.on("/Tpression", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    String sorti= sortie("/dataPress.txt",30);
    resquest->send(200, "text/plain", sorti);
    delay(200);

  });
server.on("/pression", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    String sorti= String(pression());
    resquest->send(200, "text/plain", sorti);
  });

  /////////////////////////////////////////////////////////////////////////////////////

 server.on("/humidite.html", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    resquest->send(SPIFFS, "/humidite.html", "text/html");
  });
 
  server.on("/scripthum.js", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    resquest->send(SPIFFS, "/scriptHum.js", "text/javascript");
  });
  server.on("/dataHum.txt", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    resquest->send(SPIFFS, "/dataHum.txt", "text/javascript");
  });

server.on("/Thumidite", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    String sorti= sortie("/dataHum.txt",30);
    delay(200);
    resquest->send(200, "text/plain", sorti);

  });
server.on("/humidite", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    String sorti= String(humidite());
    resquest->send(200, "text/plain", sorti);
  });
///////////////////////////////////////////////////

server.on("/Air.html", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    resquest->send(SPIFFS, "/Air.html", "text/html");
  });
 
  server.on("/scriptAir.js", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    resquest->send(SPIFFS, "/scriptAir.js", "text/javascript");
  });
  server.on("/dataAir.txt", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    resquest->send(SPIFFS, "/dataAir.txt", "text/javascript");
  });

server.on("/Tair", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    String sorti= sortie("/dataAir.txt",30);
    resquest->send(200, "text/plain", sorti);
    delay(100);

  });
server.on("/Air", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    String sorti= String(air());
    resquest->send(200, "text/plain", sorti);
  });


////////////////////////////////////////////////////////

server.on("/vent.html", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    resquest->send(SPIFFS, "/vent.html", "text/html");
  });
 
  server.on("/scriptVent.js", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    resquest->send(SPIFFS, "/scriptVent.js", "text/javascript");
  });
  server.on("/dataVent.txt", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    resquest->send(SPIFFS, "/dataVent.txt", "text/javascript");
  });

server.on("/Tvent", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    String sorti= sortie("/dataVent.txt",30);
    
    resquest->send(200, "text/plain", sorti);
  delay(100);
  });
server.on("/vent", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    String sorti= String(vent());
    resquest->send(200, "text/plain", sorti);
  });
///////////////////////////////////////
server.on("/Temperature.html", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    resquest->send(SPIFFS, "/Temperature.html", "text/html");
  });
 
  server.on("/scriptTemperature.js", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    resquest->send(SPIFFS, "/scriptTemperature.js", "text/javascript");
  });
  server.on("/dataTemp.txt", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    resquest->send(SPIFFS, "/dataTemp.txt", "text/javascript");
  });

server.on("/Ttemperature", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    String sorti= sortie("/dataTemp.txt",30);
    resquest->send(200, "text/plain", sorti);
    delay(100);

  });
server.on("/temperature", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    String sorti= String(temperature());
    resquest->send(200, "text/plain", sorti);
  });

//////////////////////////////////////////////////////////////
server.on("/Intensite.html", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    resquest->send(SPIFFS, "/Intensite.html", "text/html");
  });
 
  server.on("/scriptIntensite.js", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    resquest->send(SPIFFS, "/scriptIntensite.js", "text/javascript");
  });
  server.on("/dataIntensite.txt", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    resquest->send(SPIFFS, "/dataIntensite.txt", "text/javascript");
  });

server.on("/Tintensite", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    String sorti= sortie("/dataIntensite.txt",30);
    resquest->send(200, "text/plain", sorti);
    delay(100);

  });
server.on("/intensite", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    String sorti= String(UV());
    resquest->send(200, "text/plain", sorti);
  });

////////////////////////////////////////////////////

server.on("/pluie", HTTP_GET, [](AsyncWebServerRequest *resquest) {
    String sorti= String(volumePluie());
    resquest->send(200, "text/plain", sorti);

  });

server.begin();
Serial.println("okay server actif");
lcd.clear();
}
/////////////////////////////////////////////
void loop() {
  writeToFile("/dataPress.txt", String(pression()));
  Serial.println(pression());

  writeToFile("/dataHum.txt", String(humidite()));
  writeToFile("/dataAir.txt", String(air()));
  writeToFile("/dataVent.txt", String(vent()));
  writeToFile("/dataTemp.txt", String(temperature()));
  writeToFile("/dataIntensite.txt", String(UV()));
  GlobalWriteToFile("/GlobalData.txt",String(pression()),String(humidite()),String(air()),String(vent()),String(temperature()),String(UV()) );
  delay(500);
  afficheData();

}


