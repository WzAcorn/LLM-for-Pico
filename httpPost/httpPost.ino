#include <SPI.h>
#include <Ethernet.h>
#include <Adafruit_NeoPixel.h>

byte mac[] = { 0x00, 0x08, 0xDC, 0x92, 0x42, 0x80 }; // 임의의 MAC 주소
IPAddress ip(192, 168, 0, 20); // 고정 IP 주소 설정
IPAddress server(192, 168, 0, 5); // Flask 서버의 IP 주소
EthernetClient client;

const int ledPin = 25; // LED 핀 번호를 25로 설정
const int RGBledPin = 6; // LED 핀 번호를 25로 설정
const int BuzzerPin = 20; // LED 핀 번호를 25로 설정
Adafruit_NeoPixel strip(1, RGBledPin, NEO_GRB + NEO_KHZ800);  //LED는 1개라 count값 1.

struct DHTStruct{
  float latitude=0.0;
  float longitude=0.0;
};

struct RGBLedStruct{
  uint8_t red =0;
  uint8_t green =0;
  uint8_t blue =0;
};

struct BuzzerStruct{
  int buzzer[100];
  int noteDurations[100];
  int repeat =0;
};


struct Container{
  RGBLedStruct rgbLedStruct;
  BuzzerStruct buzzerStruct;
  DHTStruct dhtStruct;
};

Container container;


void setup() {
  Serial.begin(9600);
  strip.begin();           // NeoPixel strip 초기화
  strip.show();            // 모든 LED를 꺼서 시작(초기화 시 필요)
  pinMode(ledPin, OUTPUT); // ledPin을 출력으로 설정
  pinMode(BuzzerPin, OUTPUT); // ledPin을 출력으로 설정
  
  while (!Serial) {
    ; // 시리얼 포트가 준비될 때까지 대기
  }
  // 고정 IP 주소를 사용하여 이더넷을 구성합니다.
  //Ethernet.begin(mac,ip);
  // DHCP로 하고싶으면 아래 코드를 실행하세요.
  Ethernet.begin(mac);
  delay(500); // 네트워크 안정화를 위한 대기
  Serial.println("######Enter your query to Serial Moniter########");
}

void loop() {
  static String inputString = ""; // 사용자 입력을 저장할 문자열
  static boolean inputComplete = false; // 입력 완료 여부를 나타내는 플래그

  while (Serial.available() > 0) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') {
      inputComplete = true;
    }
  }

  if (inputComplete) {
    Serial.print("Sending query: ");
    Serial.println(inputString);
    inputString.trim(); // inputString의 앞뒤 공백 제거
    post_to_APIServer(inputString, container); // 수정된 inputString 전달
    RGBled_Control(container);
    buzzer_control(container);
    inputString = ""; // 입력 문자열 초기화
    inputComplete = false; // 입력 완료 플래그 재설정
  }
  delay(200);
}


void post_to_APIServer(String myQuery, Container &container) {
  String deviceData = "POST /sensor_Control HTTP/1.1";
  String postData = "{\"query\": \"" + myQuery + "\"}";
  String myResponse = ""; // 서버로부터의 응답을 저장할 변수
  bool isConnected = client.connect(server, 8080);
  Serial.println(isConnected);
  if (isConnected) {
    Serial.println("Connected to server");
    // HTTP 요청 전송
    client.println(deviceData);
    client.println("Host: 192.168.0.5:8080");
    client.println("Content-Type: application/json");
    client.println("Connection: close");
    client.print("Content-Length: ");
    client.println(postData.length());
    client.println();
    client.println(postData);
    // 서버로부터의 응답 읽기
    while (client.connected() || client.available()) {
      while (client.available()) {
        char c = client.read();
        myResponse += c; // 서버로부터 읽은 문자를 응답 문자열에 추가
      }
    }
    client.stop();
    
    // HTTP 응답에서 본문만 추출
    int headerEndIndex = myResponse.indexOf("\r\n\r\n") + 4;
    String responseBody = myResponse.substring(headerEndIndex);
    responseBody.trim(); // 본문의 시작과 끝의 공백 제거
    responseBody.replace("\"", "");

    // 본문 분석 및 구조체에 값 할당
    if (responseBody.startsWith("led,")) {
      int index = responseBody.indexOf(',');
      int bright = responseBody.substring(index + 1).toInt();
    } else if (responseBody.startsWith("dht,")) {
      int firstIndex = responseBody.indexOf(',');
      int secondIndex = responseBody.indexOf(',', firstIndex + 1);
      float latitude = responseBody.substring(firstIndex + 1, secondIndex).toFloat();
      float longitude = responseBody.substring(secondIndex + 1).toFloat();
      container.dhtStruct.latitude = latitude;
      container.dhtStruct.longitude = longitude;
    } else {
      Serial.println("Unknown sensor type in response.");
    }
  } else {
    Serial.println("Connection failed");
  }
}

// LED 밝기를 조절하는 함수 추가
void RGBled_Control(Container &container) {
  strip.setPixelColor(0, strip.Color(container.rgbLedStruct.red,container.rgbLedStruct.green,container.rgbLedStruct.blue));
  strip.show(); // LED 색상 업데이트
}

void buzzer_control(Container &container) {
  // 수정된 buzzer_control 함수
  uint8_t arraySize = sizeof(container.buzzerStruct.buzzer) / sizeof(container.buzzerStruct.buzzer[0]);
  for (int j = 0; j < container.buzzerStruct.repeat; j++) { // 올바른 변수 사용
    for (int i = 0; i < arraySize; i++) {
      tone(BuzzerPin, container.buzzerStruct.buzzer[i], container.buzzerStruct.noteDurations[i]);
      
      int pauseBetweenNotes = container.buzzerStruct.noteDurations[i] * 1.30;
      delay(pauseBetweenNotes);
      
      noTone(BuzzerPin);
    }
  }
  container.buzzerStruct.repeat = 0;
}
