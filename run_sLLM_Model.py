import subprocess

def run_model(executable_path, model_path, prompt, num_tokens=100, temperature=0):
    # 명령어 구성
    command = [
        executable_path, # 실행 파일 경로
        '-m', model_path, # 모델 경로
        '-p', prompt, # 프롬프트
        '-n', str(num_tokens), # 생성할 토큰 수
        '--temp', str(temperature) # 온도 설정
    ]

    # subprocess를 사용하여 외부 명령어 실행
    process = subprocess.run(command, text=True, capture_output=True)

    # 결과 출력 및 반환
    return process.stdout

# 사용 예
prompt = "tell me about BTS"
executable_path = '/home/acorn/workspace/llama.cpp/build/bin/main'
model_path = '/home/acorn/workspace/llama.cpp/AIFT-instruct-SFT-1.3B-v2.1.gguf'

output = run_model(executable_path, model_path, prompt)
print(output)
