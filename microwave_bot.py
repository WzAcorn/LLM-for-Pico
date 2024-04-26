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
# Microwave Chatbot Instructions
Please answer Your Answer by referring to the Answer Format.
Please do not give any other answer other than Your Answer.

## Answer Format
answer = {{"microwave" : , "time" : }}

## Determine Microwave Power:
Decide on the suitable microwave power setting based on the specified dish and ingredients.
Power settings generally range among 'low', 'medium', and 'high'.
### Set Cooking Time:
Determine the appropriate microwave cooking time based on the type of dish and the quantity of ingredients. Time should always be provided in seconds.


## Responses
Extract the answer from this sentence
"I want to boil an egg"
answer = {{"microwave" : "low", "time" : 360}}

Extract the answer from this sentence
"I want to cook rice"
answer = {{"microwave" : "medium", "time" : 900}}

Extract the Your answer from this sentence
{text}
Your answer =
"""
prompttemplate = PromptTemplate(template=prompt_template, input_variables=["text"])

query = "I want warm up the baguette"

llm.invoke(prompttemplate.format(text=query), max_tokens = 40)