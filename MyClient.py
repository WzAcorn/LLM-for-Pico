from langchain.chains import create_tagging_chain
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-1106")

led_Control_Schema = {
    "description": """
    - This field specifies the brightness of the light from 0 (completely off) to 255 (maximum brightness).
    - Please only use multiples of 7 to provide users with a variety of values.
    - The RGB value is determined by considering the user's situation and emotions.
    - Let's Think about it step by step.
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


query = "잔잔한 느낌으로 불을 켜줘"
chain = create_tagging_chain(led_Control_Schema, llm)
answer = chain.invoke(query)
print(answer)