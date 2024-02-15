#include <SPI.h>
#include <Ethernet.h>

byte mac[] = { 0x00, 0x08, 0xDC, 0x89, 0x42, 0x77 }; // 임의의 MAC 주소
IPAddress ip(192, 168, 0, 13); // 고정 IP 주소 설정
IPAddress server(192, 168, 0, 5); // Flask 서버의 IP 주소
EthernetClient client;

const int ledPin = 25; // LED 핀 번호를 25로 설정

struct LedStruct{
  int bright=0;
};

struct DHTStruct{
  float latitude=0.0;
  float longitude=0.0;
};

struct Container{
  LedStruct ledStruct;
  DHTStruct dhtStruct;
};

Container container;


void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT); // ledPin을 출력으로 설정
  
  while (!Serial) {
    ; // 시리얼 포트가 준비될 때까지 대기
  }
  // 고정 IP 주소를 사용하여 이더넷을 구성합니다.
  Ethernet.begin(mac,ip);
  delay(1000); // 네트워크 안정화를 위한 대기
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
    post_to_APIServer("led_Control",inputString,container); // 수정된 inputString 전달
    Led_Control(container.ledStruct.bright);
    inputString = ""; // 입력 문자열 초기화
    inputComplete = false; // 입력 완료 플래그 재설정
  }
  delay(200);
}


void post_to_APIServer(String device, String myQuery, Container &container) {
  String deviceData = "POST /" + device + " HTTP/1.1";
  String postData = "{\"query\": \"" + myQuery + "\"}";
  String myResponse = ""; // 서버로부터의 응답을 저장할 변수
  
  if (client.connect(server, 8080)) {
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
      container.ledStruct.bright = bright;
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
void Led_Control(uint8_t bright) {
  analogWrite(ledPin, bright); // LED 밝기 설정
  Serial.println("LED Brightness: " + String(bright));
}
