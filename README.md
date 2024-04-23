# LLM for Pico
 c++로 Pico에서 LLM을 사용할 수 있게 하는 프로젝트

### 진행사항


### 라즈베리파이 실행명령어
- 가상환경 활성화 : source ~/venvs/llm-pico/bin/activate
- 파일 실행 방법 : [가상환경 경로 내 파일위치]  
- 내 flask 서버 실행 : /home/acorn/venvs/llm-pico/bin/python /home/acorn/workspace/LLM-for-Pico/
MyServer.py
- 모델 실행 : ./main -m acorn_tinyllama -p "your prompt" -n 200