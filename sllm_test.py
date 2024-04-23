from langchain_community.llms import LlamaCpp

llm = LlamaCpp(
    model_path="/home/acorn/workspace/llama.cpp/AIFT-instruct-SFT-1.3B-v2.1.gguf",
    max_tokens = 100,
    n_gpu_layers=1,
    n_batch=128,
    n_ctx=512,
    f16_kv=True,
    verbose=False,
)

prompt = "BTS 멤버 이름 전부 말해줘."
output = llm.invoke(prompt)
print(output)