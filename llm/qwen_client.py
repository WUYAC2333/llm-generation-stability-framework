from dashscope import Generation

def call_qwen(prompt: str,
              temperature: float = 0.3,
              max_tokens: int = 2048) -> str:

    response = Generation.call(
        model="qwen-max",
        messages=[{"role": "user", "content": prompt}],
        result_format="message",
        temperature=temperature,
        max_tokens=max_tokens
    )

    if response.status_code != 200:
        raise RuntimeError(f"Qwen API Error: {response.status_code}")

    return response.output.choices[0].message.content