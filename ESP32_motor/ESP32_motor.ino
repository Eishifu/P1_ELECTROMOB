// ESP32 open server on port 10000 to receive a flaot

#include <WiFi.h>

// Replace with your network credentials
const char* ssid = "Pixel_2844";
const char* password= "Tortue22";
//"ELECTROMOB""ProjectP1", "Pixel_2844""Tortue22", "NETGEAR_11N""sharedsecret"
WiFiServer server(10000);  // server port to listen on

// Button
int bsignal = 0;
bool alreadynoclient=false;
bool alreadynoWiFi=false;
bool alreadyConnected = false;  // whether or not the client was connected previously
const int pinconv=22;
const int pininj=23;

//Motor
const int motorPin1 = 13; //sens horaire// input 4 sur la carte rouge
const int motorPin2 = 15; //sens antihoraire //input 3 sur la carte rouge
const int pinfdc1 = 4;
const int pinfdc2 = 21;
int speed = 180;
int fdc1;
int fdc2;
float sendValue;
void setup() {
  Serial.begin(115200);
  //Buttons
  pinMode(pininj, INPUT);
  pinMode(pinfdc1, INPUT);
  pinMode(pinfdc2, INPUT);
  pinMode(pinconv,INPUT);
  //Motor
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
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
    if (!alreadynoclient and WiFi.status() == WL_CONNECTED ){
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
        if (value == 50){
          fdc1=digitalRead(pinfdc1);
          Serial.println("Closing");
          analogWrite(motorPin2,speed);
          sendValue = 2;
          client.write((const uint8_t*)&sendValue, sizeof(sendValue));
          Serial.printf("Sent back value due to the start of operation: %f\n", sendValue);
          while(fdc1!=1){
            fdc1=digitalRead(pinfdc1);
            //Serial.println(fdc1);
          }
          analogWrite(motorPin2, 0); 
          Serial.println("Closed");
          sendValue = 3;
          client.write((const uint8_t*)&sendValue, sizeof(sendValue));
          Serial.printf("Sent back value due to succes of operation: %f\n", sendValue);
        }else if(value == 51){
          fdc2=digitalRead(pinfdc2);
          Serial.println("Opening");
          analogWrite(motorPin1,speed);
          sendValue = 2;
          client.write((const uint8_t*)&sendValue, sizeof(sendValue));
          Serial.printf("Sent back value due to the start of operation: %f\n", sendValue);
          while(fdc2!=1){
            fdc2=digitalRead(pinfdc2);
            //Serial.println(fdc2);
          }
          analogWrite(motorPin1, 0);
          Serial.println("Opened");
          sendValue = 3;
          client.write((const uint8_t*)&sendValue, sizeof(sendValue));
          Serial.printf("Sent back value due to succes of operation: %f\n", sendValue);
        }else {
          bsignal= digitalRead(value);
          Serial.printf("Pin to read: %f\n", value);
          sendValue = bsignal;
          client.write((const uint8_t*)&sendValue, sizeof(sendValue));
          Serial.printf("Sent back value of pin: %f\n", sendValue);
        }
      } else
        while (client.available()) Serial.print((char)client.read());  // discard corrupt packet
    }
  }
  if (WiFi.status()==WL_CONNECTED && alreadynoWiFi){
    alreadynoWiFi=false;
    Serial.print("Connected to :");
    Serial.println(WiFi.SSID());
    }
  if(WiFi.status()!=WL_CONNECTED && !alreadynoWiFi){
    Serial.println("Disconnected");
    alreadynoWiFi=true;
    alreadynoclient=false;
  }
  fdc2=digitalRead(pinfdc2);
  fdc1=digitalRead(pinfdc1);
  if (fdc2==1) {analogWrite(motorPin1, 0);}
  if (fdc1==1) {analogWrite(motorPin2, 0);}
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