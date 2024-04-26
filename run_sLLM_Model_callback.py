from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import StreamingStdOutCallbackHandler, CallbackManager
from langchain_core.prompts import PromptTemplate

# 모델 파일 경로 지정
model_path = "/home/acorn/workspace/LLM-for-Pico/Phi-3-mini-4k-instruct-q4.gguf"

# 콜백 핸들러 설정
callback_handler = StreamingStdOutCallbackHandler()
callback_manager = CallbackManager([callback_handler])

# LlamaCpp 인스턴스 생성 (콜백 매니저 전달)
llm = LlamaCpp(model_path=model_path, 
                callback_manager=callback_manager,
                n_ctx=512,
                n_batch=4,
                temperature = 0,
                verbose=False)

# 프롬프트 템플릿 정의
prompt_template = """
Answer Format를 참고하여 Your Answer를 대답해주세요.
반드시 Your Answer 이외에 어떠한 다른 대답도 하지 말아주세요.

### Answer Format
answer = {{"movie name": , "critic": , "Positive/Negative": , "grade" : }}

### Example
다음 영화 리뷰에서 answer를 추출하세요:
Review of The Batman by christoper nolan : This is the greatest action movie ever made. 5 out of 5 stars.

answer = {{"movie name": The Batman, "critic": christoper nolan , "Positive/Negative": positive, "grade" : 5}}

다음 영화 리뷰에서 Your answer를 추출하세요:
{text}
Your Answer =
"""
prompttemplate = PromptTemplate(template=prompt_template, input_variables=["text"])

query = "Review of The Bee Movie by Roger Ebert: This is the greatest movie ever made. 4 out of 5 stars."

result = llm.invoke(prompttemplate.format(text=query), max_tokens = 45)
print(result)