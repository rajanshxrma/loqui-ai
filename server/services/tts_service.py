import boto3
from config import settings


# language → polly voice mapping (neural voices)
VOICE_MAP = {
    "en": {"voice_id": "Joanna", "engine": "neural"},
    "es": {"voice_id": "Lucia", "engine": "neural"},
    "fr": {"voice_id": "Lea", "engine": "neural"},
    "de": {"voice_id": "Vicki", "engine": "neural"},
    "ja": {"voice_id": "Takumi", "engine": "neural"},
    "zh": {"voice_id": "Zhiyu", "engine": "neural"},
    "ko": {"voice_id": "Seoyeon", "engine": "neural"},
    "pt": {"voice_id": "Camila", "engine": "neural"},
    "hi": {"voice_id": "Kajal", "engine": "neural"},
    "ar": {"voice_id": "Zayd", "engine": "neural"},
}


def _get_polly_client():
    return boto3.client(
        "polly",
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )


def synthesize_speech(text, language="en"):
    """convert text to speech using aws polly neural voices"""
    voice_config = VOICE_MAP.get(language, VOICE_MAP["en"])
    client = _get_polly_client()

    response = client.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId=voice_config["voice_id"],
        Engine=voice_config["engine"],
    )

    if "AudioStream" in response:
        return response["AudioStream"].read()

    raise Exception("polly returned no audio stream")


def get_supported_languages():
    """return list of supported language codes and their voice info"""
    return {
        code: {
            "voice": config["voice_id"],
            "engine": config["engine"],
        }
        for code, config in VOICE_MAP.items()
    }
