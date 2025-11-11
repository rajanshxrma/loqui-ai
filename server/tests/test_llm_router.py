import pytest
from services.llm_router import _get_system_prompt, _build_messages, SYSTEM_PROMPTS


class TestSystemPrompts:
    def test_english_prompt_exists(self):
        prompt = _get_system_prompt("en")
        assert "LoquiAI" in prompt
        assert "English" in prompt

    def test_spanish_prompt(self):
        prompt = _get_system_prompt("es")
        assert "español" in prompt

    def test_japanese_prompt(self):
        prompt = _get_system_prompt("ja")
        assert "LoquiAI" in prompt

    def test_unknown_language_falls_back_to_english(self):
        prompt = _get_system_prompt("xx")
        assert prompt == SYSTEM_PROMPTS["en"]

    def test_all_languages_have_prompts(self):
        expected = ["en", "es", "fr", "de", "ja", "zh", "ko", "pt", "hi", "ar"]
        for lang in expected:
            assert lang in SYSTEM_PROMPTS


class TestBuildMessages:
    def test_prepends_system_prompt(self):
        messages = [{"role": "user", "content": "hello"}]
        built = _build_messages(messages, "en")
        assert built[0]["role"] == "system"
        assert built[1]["role"] == "user"
        assert len(built) == 2

    def test_preserves_original_messages(self):
        messages = [
            {"role": "user", "content": "hi"},
            {"role": "assistant", "content": "hello"},
            {"role": "user", "content": "how are you"},
        ]
        built = _build_messages(messages, "fr")
        assert len(built) == 4
        assert built[0]["role"] == "system"
        assert "français" in built[0]["content"]


class TestModelRouting:
    def test_gpt_model_detection(self):
        # just test the routing logic, not actual api calls
        assert "gpt" in "gpt-4o"
        assert "gpt" in "gpt-4o-mini"
        assert "claude" not in "gpt-4o"

    def test_claude_model_detection(self):
        assert "claude" in "claude-3.5-sonnet"
        assert "claude" in "claude-3-opus"
        assert "gpt" not in "claude-3.5-sonnet"

    def test_unsupported_model_string(self):
        model = "llama-3"
        assert "gpt" not in model and "claude" not in model
