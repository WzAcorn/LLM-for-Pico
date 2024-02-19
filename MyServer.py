from flask import Flask, request, jsonify
import requests
import json
from langchain.chains import create_tagging_chain
from langchain.chat_models import ChatOpenAI
from waitress import serve
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 파일 로깅 핸들러 추가
file_handler = RotatingFileHandler('serverLog.log', maxBytes=10240, backupCount=5)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# llm과 각 센서별 스키마 정의.
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-1106")
led_Control_Schema = {
    "description": """
    - This field specifies the brightness of the light from 0 (completely off) to 255 (maximum brightness).
    - Please only use multiples of 7 to provide users with a variety of values.
    - The RGB value is determined by considering the user's situation and emotions.
    - Let's Think about step by step.
    """,
    "properties": {
        "red": {
            "type": "integer",
            "minimum": 0,  # 최소값을 0으로 설정
            "maximum": 255,  # 최대값을 255로 설정
            "description": "This column is the red value of RGBleb, which means aggressive, passionate, and loving.",
        },
        "green": {
            "type": "integer",
            "minimum": 0,  # 최소값을 0으로 설정
            "maximum": 255,  # 최대값을 255로 설정
            "description": "This column is the green value of RGBleb, meaning calm, stable, and neutral.",
        },
        "blue": {
            "type": "integer",
            "minimum": 0,  # 최소값을 0으로 설정
            "maximum": 255,  # 최대값을 255로 설정
            "description": "This column is the blue value of RGBleb, meaning gloomy, fearful, and negative.",
        },
                        
    },
    "required": ["red","green","blue"]
}

buzzer_Control_Schema = {
  "description": "This scheme is used to buzzer in picobricks. You can control the buzzer through picobricks by defining the melody, the duration of the notes, and the number of repetitions of the buzzer. let's think about step by step.",
  "properties": {
    "buzzer": {
      "type": "array",
      "items": {
        "type": "integer",
        "maximum" : 1024
      },
      "description": "An array of frequencies in Hz for each note in the buzzer. Each value must be an integer representing the frequency."
    },
    "noteDurations": {
      "type": "array",
      "items": {
        "type": "integer",
        "minimum": 1  # 지속 시간은 최소 1ms 이상이어야 합니다.
      },
      "description": "An array of durations in milliseconds for each note in the buzzer. Each value must be an integer representing the duration."
    },
    "repeat": {
      "type": "integer",
      "minimum": 1,  # 반복 횟수는 최소 1이어야 합니다.
      "description": "The number of times the buzzer should be repeated. Must be a positive integer."
    }
  },
  "required": ["buzzer", "noteDurations", "repeat"]
}

devide_Sensor = {
    "description": """
    - This request parses the user's request and returns one of the picobricks sensors.
    - Let's Think about it step by step.
    """,
    "properties": {
        "sensor": {
            "type": "integer",
            "enum": ["LED", "BUZZER", "MONITER","DHT", "RELAY","LDR","WIRELESS"],
            "description": "This column is the red value of RGBleb, which means aggressive, passionate, and loving.",
        },                   
    },
    "required": ["sensor"]
    
}



@app.route('/sensor_Control', methods=['POST'])
def sensor_Control():
    user_ip = request.remote_addr  # 요청한 사용자의 IP 주소
    data = request.json
    query = data['query']
    if not query:
        logger.error(f"No query provided from {user_ip}")
        return jsonify({'error': 'No query provided'}), 400

    logger.info(f"Request {user_ip}: {query}")  # 로그에 요청 데이터와 사용자 IP 기록

    #어떤 센서값의 요청인지 분리하는 코드.
    try:
        chain = create_tagging_chain(devide_Sensor, llm)
        answer = chain.invoke(query)
        task_sensor = answer['text']['sensor']
        if task_sensor == "LED":
            chain = create_tagging_chain(led_Control_Schema, llm)
            answer = chain.invoke(query)
            return jsonify(answer)
        if task_sensor == "BUZZER":
            chain = create_tagging_chain(buzzer_Control_Schema, llm)
            answer = chain.invoke(query)
            return jsonify(answer)
        
        logger.info(f"Response {user_ip}: {answer}")  # 로그에 응답 데이터와 사용자 IP 기록
    except Exception as e:
        logger.error(f"Error occurred: {str(e)} from {user_ip}")  # 로그에 오류 메시지와 사용자 IP 기록
        return jsonify({'error': str(e)}), 500




if __name__ == '__main__':
    # 프로덕션 환경에서는 Waitress 서버를 사용
    serve(app, host='0.0.0.0', port=8080)
