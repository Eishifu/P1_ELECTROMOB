// ESP32 open server on port 10000 to receive a float pin id and send back pin value

#include <WiFi.h>

// Replace with your network credentials
const char* ssid = "Pixel_2844";
const char* password = "Tortue22";
//"ELECTROMOB""ProjectP1", "Pixel_2844""Tortue22"
WiFiServer server(10000);  // server port to listen on

// Button
int bsignal = 0;
bool alreadynoclient=false;
bool alreadynoWiFi=false;
bool alreadyConnected = false;  // whether or not the client was connected previously


void setup() {
  Serial.begin(115200);
  //Button
  pinMode(2,INPUT);
  pinMode(4,INPUT);
  pinMode(21,INPUT);
  pinMode(22,INPUT);
  pinMode(23,INPUT);
  // setup Wi-Fi network with SSID and password
  Serial.printf("Connecting to %s\n", ssid);
  Serial.printf("\nattempting to connect to WiFi network SSID '%s' password '%s' \n", ssid, password);
  // attempt to connect to Wifi network:
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(500);
  }
  server.begin();
  // you're connected now, so print out the status:
  printWifiStatus();
  Serial.println(" listening on port 10000");
}



void loop() {
  static WiFiClient client;
  //static int16_t seqExpected = 0; removed
  if (!client){
    client = server.available();  // Listen for incoming clients
    alreadyConnected = false;
    if (!alreadynoclient){
      Serial.println("Waiting for client");
      alreadynoclient=true;
    }
  }
  if (client) {                   // if client connected
    alreadynoclient=false;
    if (!alreadyConnected) {
      // clead out the input buffer:
      client.flush();
      Serial.println("We have a new client");
      alreadyConnected = true;
    }
    // if data available from client read and display it
    int length;
    float value;
    if ((length = client.available()) > 0) {
      //str = client.readStringUntil('\n');  // read entire response
      // if data is correct length read and display it
      if (length == sizeof(value)) {
        client.readBytes((char*)&value, sizeof(value));
        bsignal= digitalRead(value);
        Serial.printf("Pin to read: %f\n", value);
        float sendValue = bsignal;
        client.write((const uint8_t*)&sendValue, sizeof(sendValue));
        Serial.printf("Sent back value: %f\n", sendValue);
        }
      } else
        while (client.available()) Serial.print((char)client.read());  // discard corrupt packet
  }
  if (WiFi.status()==WL_CONNECTED && alreadynoWiFi){alreadynoWiFi=false;Serial.print("Connected to :");Serial.println(WiFi.SSID());}
  if(WiFi.status()!=WL_CONNECTED && !alreadynoWiFi){
    Serial.println("Disconnected");
    alreadynoWiFi=true;
    alreadynoclient=false;
  }
}


void printWifiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("\nSSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}