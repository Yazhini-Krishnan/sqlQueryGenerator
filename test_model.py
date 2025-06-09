from llama_cpp import Llama

# Use the printed path from previous step
MODEL_PATH = "/Users/yazhini.krishnan/.cache/huggingface/hub/models--microsoft--Phi-3-mini-4k-instruct-gguf/snapshots/999f761fe19e26cf1a339a5ec5f9f201301cbb83/Phi-3-mini-4k-instruct-q4.gguf"

llm = Llama(model_path=MODEL_PATH)

prompt = (
    "You are a helpful assistant that writes SQL queries.\n"
    "Table schema: users(id INT, name VARCHAR, revenue FLOAT)\n"
    "User request: Find the top 5 users by revenue.\n"
    "SQL:"
)
output = llm(prompt, max_tokens=256)
print(output['choices'][0]['text'])