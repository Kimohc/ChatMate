import openai


def send_request_to_ai(message: str):
    client = openai.OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    completion = client.chat.completions.create(
        model="TheBloke/dolphin-2_6-phi-2-GGUF",
        messages=[
            {"role": "system", "content": "You are a woman on a dating app chatting with the love of your life."},
            {"role": "user", "content": message}
        ],
        temperature=0.7,
    )

    return completion.choices[0].message

