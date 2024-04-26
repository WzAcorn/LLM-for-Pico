from langchain_community.llms import LlamaCpp

# 모델 파일 경로 지정
model_path = "/home/acorn/workspace/LLM-for-Pico/Phi-3-mini-4k-instruct-q4.gguf"

# LlamaCpp 인스턴스 생성 (콜백 매니저 전달)
llm = LlamaCpp(model_path=model_path, 
                n_ctx=512,
                n_batch=4,
                max_token=50,
                temperature=0,
                verbose=True)

# 모델에 텍스트 입력하고 출력 받기
text = "How many members are there in BTS?"
print(llm.invoke(text))
