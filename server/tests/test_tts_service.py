from services.tts_service import VOICE_MAP, get_supported_languages


class TestVoiceMapping:
    def test_english_voice(self):
        assert VOICE_MAP["en"]["voice_id"] == "Joanna"
        assert VOICE_MAP["en"]["engine"] == "neural"

    def test_all_languages_have_voices(self):
        expected = ["en", "es", "fr", "de", "ja", "zh", "ko", "pt", "hi", "ar"]
        for lang in expected:
            assert lang in VOICE_MAP
            assert "voice_id" in VOICE_MAP[lang]
            assert "engine" in VOICE_MAP[lang]

    def test_all_voices_are_neural(self):
        for lang, config in VOICE_MAP.items():
            assert config["engine"] == "neural", f"{lang} is not neural"

    def test_no_duplicate_voices(self):
        voice_ids = [config["voice_id"] for config in VOICE_MAP.values()]
        assert len(voice_ids) == len(set(voice_ids))

    def test_get_supported_languages(self):
        languages = get_supported_languages()
        assert isinstance(languages, dict)
        assert "en" in languages
        assert "voice" in languages["en"]
        assert languages["en"]["voice"] == "Joanna"
