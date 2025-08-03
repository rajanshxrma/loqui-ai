import openai
import anthropic
from config import settings


# language-aware system prompts
SYSTEM_PROMPTS = {
    "en": "You are LoquiAI, a helpful multilingual assistant. Respond in English. Be concise and helpful.",
    "es": "Eres LoquiAI, un asistente multilingüe. Responde en español. Sé conciso y útil.",
    "fr": "Vous êtes LoquiAI, un assistant multilingue. Répondez en français. Soyez concis et utile.",
    "de": "Sie sind LoquiAI, ein mehrsprachiger Assistent. Antworten Sie auf Deutsch. Seien Sie prägnant und hilfreich.",
    "ja": "あなたはLoquiAIです。日本語で応答してください。簡潔で役立つ回答をしてください。",
    "zh": "你是LoquiAI，一个多语言助手。请用中文回答。回答要简洁有用。",
    "ko": "당신은 LoquiAI입니다. 한국어로 답변해 주세요. 간결하고 유용하게 답변하세요.",
    "pt": "Você é o LoquiAI, um assistente multilíngue. Responda em português. Seja conciso e útil.",
    "hi": "आप LoquiAI हैं, एक बहुभाषी सहायक। हिंदी में जवाब दें। संक्षिप्त और सहायक रहें।",
    "ar": "أنت LoquiAI، مساعد متعدد اللغات. أجب بالعربية. كن موجزاً ومفيداً.",
}


def _get_system_prompt(language):
    return SYSTEM_PROMPTS.get(language, SYSTEM_PROMPTS["en"])


def _build_messages(messages, language):
    """prepend system prompt with language context"""
    system_msg = {"role": "system", "content": _get_system_prompt(language)}
    return [system_msg] + messages


# lazy client init so tests don't crash without api keys
_openai_client = None
_anthropic_client = None


def _get_openai_client():
    global _openai_client
    if _openai_client is None:
        _openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    return _openai_client


def _get_anthropic_client():
    global _anthropic_client
    if _anthropic_client is None:
        _anthropic_client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
    return _anthropic_client


async def stream_response(model, messages, language="en"):
    """unified streaming router — yields tokens from either provider"""
    full_messages = _build_messages(messages, language)

    if "gpt" in model or "openai" in model:
        stream = await _get_openai_client().chat.completions.create(
            model=model,
            messages=full_messages,
            stream=True,
            temperature=0.7,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                yield delta.content

    elif "claude" in model or "anthropic" in model:
        # anthropic expects system prompt separately
        system_prompt = _get_system_prompt(language)
        user_messages = [m for m in messages if m["role"] != "system"]

        async with _get_anthropic_client().messages.stream(
            model=model,
            system=system_prompt,
            messages=user_messages,
            max_tokens=2048,
            temperature=0.7,
        ) as stream:
            async for text in stream.text_stream:
                yield text

    else:
        raise ValueError(f"unsupported model: {model}")


async def get_response(model, messages, language="en"):
    """non-streaming — collect full response"""
    tokens = []
    async for token in stream_response(model, messages, language):
        tokens.append(token)
    return "".join(tokens)
