from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()
HF_TOKEN = os.getenv("HUG_API_KEY", None)


def ask_llm(prompt: str, system: str = "You are a concise research assistant."):
    """Query a Hugging Face hosted LLM."""
    client = InferenceClient(token=HF_TOKEN)
    model_id = "mistralai/Mistral-7B-Instruct-v0.2"  # change if desired
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt},
    ]
    try:
        response = client.chat_completion(model=model_id, messages=messages, max_tokens=1500, temperature=0.3)
        return response.choices[0].message["content"]
    except Exception as e:
        return f"Error calling model: {e}"

