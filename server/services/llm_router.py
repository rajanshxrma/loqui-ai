import openai
from config import settings

openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

SYSTEM_PROMPTS = {
    "en": "You are LoquiAI, a helpful multilingual assistant. Respond in English. Be concise and helpful.",
}

def _get_system_prompt(language):
    return SYSTEM_PROMPTS.get(language, SYSTEM_PROMPTS["en"])

def _build_messages(messages, language):
    system_msg = {"role": "system", "content": _get_system_prompt(language)}
    return [system_msg] + messages

async def stream_response(model, messages, language="en"):
    full_messages = _build_messages(messages, language)
    stream = await openai_client.chat.completions.create(
        model=model, messages=full_messages, stream=True, temperature=0.7,
    )
    async for chunk in stream:
        delta = chunk.choices[0].delta
        if delta.content:
            yield delta.content

async def get_response(model, messages, language="en"):
    tokens = []
    async for token in stream_response(model, messages, language):
        tokens.append(token)
    return "".join(tokens)
