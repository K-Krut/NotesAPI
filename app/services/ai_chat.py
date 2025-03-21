from openai import OpenAI

from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_summary(text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[
            {
                "role": "user",
                "content": f"Please summarize the following text:\n{text}"
            }
        ]
    )
    return response.choices[0].message.content
