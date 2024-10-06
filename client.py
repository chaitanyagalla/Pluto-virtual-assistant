from openai import OpenAI

client= OpenAI(
    api_key = "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"
)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
        {
            "role": "user",
            "content": "what is coding"
        }
    ]
)

print(completion.choices[0].message)
