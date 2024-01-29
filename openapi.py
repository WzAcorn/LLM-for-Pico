import requests
import json

api_key = "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"  # OpenAI API 키를 입력하세요.
headers = {
    "Authorization": "Bearer " + api_key,
    "Content-Type": "application/json"
}

data = {
    "model": "gpt-3.5-turbo",  # 사용하려는 모델을 지정하세요.
    "messages": [
        {"role": "user", "content": "Translate the following English text to French: '나는 도토리야'"}  # 사용자의 메시지
    ],
    "temperature": 0,
    "max_tokens": 1024
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(data))
result = response.json()

print(result)
print(result['choices'][0]['message']['content'])
