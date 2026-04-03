"""Unit and integration tests for PromptGenerator with MiniMax provider."""
import os
from unittest.mock import MagicMock, patch

import pytest

from chatGPTMidJourneyPrompt.chatbots.minimax import ChatbotMiniMax
from chatGPTMidJourneyPrompt.mjPrompt import PromptGenerator


def _make_response(content: str):
    msg = MagicMock()
    msg.content = content
    choice = MagicMock()
    choice.message = msg
    resp = MagicMock()
    resp.choices = [choice]
    return resp


def _mock_minimax_bot(return_text: str):
    """Return a patched ChatbotMiniMax whose ask() returns *return_text*."""
    with patch("chatGPTMidJourneyPrompt.chatbots.minimax.OpenAI") as mock_openai:
        bot = ChatbotMiniMax(api_key="test-key")
    bot.client.chat.completions.create.return_value = _make_response(return_text)
    return bot


class TestPromptGeneratorMiniMaxInit:
    def test_minimax_provider_creates_chatbot_minimax(self):
        config = {"provider": "minimax", "minimax_api_key": "test-key"}
        with patch("chatGPTMidJourneyPrompt.chatbots.minimax.OpenAI"):
            pg = PromptGenerator(config)
        assert isinstance(pg.chatbot, ChatbotMiniMax)

    def test_minimax_api_key_from_env(self, monkeypatch):
        monkeypatch.setenv("MINIMAX_API_KEY", "env-key")
        config = {"provider": "minimax"}
        with patch("chatGPTMidJourneyPrompt.chatbots.minimax.OpenAI") as mock_openai:
            pg = PromptGenerator(config)
        mock_openai.assert_called_once()
        call_kwargs = mock_openai.call_args[1]
        assert call_kwargs["api_key"] == "env-key"

    def test_minimax_missing_api_key_raises(self, monkeypatch):
        monkeypatch.delenv("MINIMAX_API_KEY", raising=False)
        config = {"provider": "minimax"}
        with pytest.raises(ValueError, match="MINIMAX_API_KEY"):
            PromptGenerator(config)

    def test_minimax_custom_model_forwarded(self):
        config = {
            "provider": "minimax",
            "minimax_api_key": "test-key",
            "minimax_model": "MiniMax-M2.7-highspeed",
        }
        with patch("chatGPTMidJourneyPrompt.chatbots.minimax.OpenAI"):
            pg = PromptGenerator(config)
        assert pg.chatbot.model == "MiniMax-M2.7-highspeed"

    def test_minimax_temperature_forwarded(self):
        config = {
            "provider": "minimax",
            "minimax_api_key": "test-key",
            "temperature": "0.3",
        }
        with patch("chatGPTMidJourneyPrompt.chatbots.minimax.OpenAI"):
            pg = PromptGenerator(config)
        assert pg.chatbot.temperature == pytest.approx(0.3)

    def test_default_provider_uses_v3_with_api_key(self):
        """Existing behaviour: api_key -> ChatbotV3."""
        config = {"api_key": "openai-key"}
        with patch("chatGPTMidJourneyPrompt.mjPrompt.ChatbotV3") as mock_v3:
            pg = PromptGenerator(config)
        mock_v3.assert_called_once_with("openai-key")


class TestPromptGeneratorMiniMaxV5:
    def _pg(self, response_text: str):
        config = {"provider": "minimax", "minimax_api_key": "test-key"}
        with patch("chatGPTMidJourneyPrompt.chatbots.minimax.OpenAI"):
            pg = PromptGenerator(config)
        pg.chatbot.client.chat.completions.create.return_value = _make_response(response_text)
        return pg

    def test_v5_contains_version_flag(self):
        pg = self._pg("a scenic landscape::5, mountains::4")
        result = pg.V5("mountains")
        assert "--v 5" in result

    def test_v5_removes_surrounding_quotes(self):
        pg = self._pg('"a scenic landscape::5"')
        result = pg.V5("test")
        assert not result.startswith('"')

    def test_v4_contains_version_flag(self):
        pg = self._pg("futuristic city::5, neon lights::3")
        result = pg.V4("futuristic city")
        assert "--v 4" in result

    def test_niji_contains_niji_flag(self):
        pg = self._pg("anime warrior::5, katana::4")
        result = pg.niji("anime warrior")
        assert "--niji" in result

    def test_testp_contains_testp_flag(self):
        pg = self._pg("portrait of a mage::5")
        result = pg.testp("mage portrait")
        assert "--testp" in result

    def test_v5_with_aspect_ratio(self):
        pg = self._pg("forest::5, ancient trees::4")
        result = pg.V5("forest", config={"aspect_ratio": "16:9"})
        assert "--ar 16:9" in result

    def test_v5_with_url_prefix(self):
        pg = self._pg("cyber cat::5")
        result = pg.V5("cyber cat", config={"url": "https://example.com/ref.jpg"})
        assert result.startswith("https://example.com/ref.jpg")

    def test_v5_with_color(self):
        pg = self._pg("dragon::5, fire::4")
        result = pg.V5("dragon", config={"color": "red"})
        assert "red::10" in result


class TestMiniMaxIntegration:
    """Integration-style tests that exercise the full call stack (API still mocked)."""

    def test_full_v5_generation_flow(self):
        gpt_response = "ethereal forest::5, ancient trees::4, misty light::3"
        config = {
            "provider": "minimax",
            "minimax_api_key": "test-key",
            "minimax_model": "MiniMax-M2.7",
        }
        with patch("chatGPTMidJourneyPrompt.chatbots.minimax.OpenAI"):
            pg = PromptGenerator(config)
        pg.chatbot.client.chat.completions.create.return_value = _make_response(gpt_response)

        result = pg.V5("ancient forest")

        assert gpt_response in result
        assert "--v 5" in result
        assert "--s 1000" in result
        assert "--q 2" in result

    def test_env_key_end_to_end(self, monkeypatch):
        monkeypatch.setenv("MINIMAX_API_KEY", "real-minimax-key")
        gpt_response = "samurai warrior::5, katana::4"
        with patch("chatGPTMidJourneyPrompt.chatbots.minimax.OpenAI") as mock_openai:
            pg = PromptGenerator({"provider": "minimax"})
        pg.chatbot.client.chat.completions.create.return_value = _make_response(gpt_response)

        result = pg.niji("samurai", config={"model": "artistic"})

        assert "--niji" in result
        assert gpt_response in result
