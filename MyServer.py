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
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
led_Control_Schema = {
    "properties": {
        "brightness of lights": {
            "type": "integer",
            "minimum": 0,  # 최소값을 0으로 설정
            "maximum": 255,  # 최대값을 255로 설정
            "description": "This field specifies the brightness of lights, from 0 (completely off) to 255 (full brightness). Be sure to use only multiples of 7 to give users a variety of values. Consider the user's situation and emotions to come up with an appropriate brightness. Let's Think about step by step",
        },
    },
    "required": ["brightness of lights"]
}

@app.route('/led_Control', methods=['POST'])
def generate_text():
    user_ip = request.remote_addr  # 요청한 사용자의 IP 주소
    data = request.json
    query = data['query']
    if not query:
        logger.error(f"No query provided from {user_ip}")
        return jsonify({'error': 'No query provided'}), 400

    logger.info(f"Request {user_ip}: {query}")  # 로그에 요청 데이터와 사용자 IP 기록

    try:
        chain = create_tagging_chain(led_Control_Schema, llm)
        answer = chain.invoke(query)
        output = "led," + str(answer['text']['brightness of lights'])
        logger.info(f"Response {user_ip}: {output}")  # 로그에 응답 데이터와 사용자 IP 기록
        return jsonify(output)
    except Exception as e:
        logger.error(f"Error occurred: {str(e)} from {user_ip}")  # 로그에 오류 메시지와 사용자 IP 기록
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # 프로덕션 환경에서는 Waitress 서버를 사용
    serve(app, host='0.0.0.0', port=8080)
