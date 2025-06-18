# qwen_client.py

import os
from llama_cpp import Llama

class QwenClient:
    def __init__(self, model_path: str):
        self.llm = Llama(model_path=model_path, n_ctx=2048, n_gpu_layers=-1)

    def generate_response(self, prompt: str, max_tokens: int = 500):
        # Add a system prompt to guide the model for question answering
        formatted_prompt = f"""<|im_start|>system\nYou are a helpful assistant. Answer the question accurately and concisely.\n<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"""
        output = self.llm(formatted_prompt, max_tokens=max_tokens, stop=["<|im_end|>", "\n"], echo=False)
        return output["choices"][0]["text"]


