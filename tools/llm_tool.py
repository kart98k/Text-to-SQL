import os
from anthropic import Anthropic

def ask_claude(api_key, prompt):
    model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")

    client = Anthropic(api_key=api_key)

    msg = client.messages.create(
        model=model,
        max_tokens=1000,
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return msg.content[0].text.strip()