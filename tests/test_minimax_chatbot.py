"""Unit tests for the MiniMax chatbot backend."""
import os
from unittest.mock import MagicMock, patch

import pytest

from chatGPTMidJourneyPrompt.chatbots.minimax import (
    MINIMAX_API_BASE,
    MINIMAX_DEFAULT_MODEL,
    ChatbotMiniMax,
)


def _make_response(content: str):
    """Build a minimal OpenAI-style chat completion mock."""
    msg = MagicMock()
    msg.content = content
    choice = MagicMock()
    choice.message = msg
    resp = MagicMock()
    resp.choices = [choice]
    return resp


class TestChatbotMiniMaxInit:
    def test_default_model(self):
        with patch("chatGPTMidJourneyPrompt.chatbots.minimax.OpenAI") as mock_openai:
            bot = ChatbotMiniMax(api_key="test-key")
        assert bot.model == MINIMAX_DEFAULT_MODEL

    def test_custom_model(self):
        with patch("chatGPTMidJourneyPrompt.chatbots.minimax.OpenAI"):
            bot = ChatbotMiniMax(api_key="test-key", model="MiniMax-M2.7-highspeed")
        assert bot.model == "MiniMax-M2.7-highspeed"

    def test_openai_client_receives_minimax_base_url(self):
        with patch("chatGPTMidJourneyPrompt.chatbots.minimax.OpenAI") as mock_openai:
            ChatbotMiniMax(api_key="test-key")
        mock_openai.assert_called_once_with(api_key="test-key", base_url=MINIMAX_API_BASE)

    def test_temperature_default(self):
        with patch("chatGPTMidJourneyPrompt.chatbots.minimax.OpenAI"):
            bot = ChatbotMiniMax(api_key="test-key")
        assert bot.temperature == 0.7

    def test_temperature_clamped_to_min(self):
        """MiniMax rejects temperature=0.0; clamp to 0.01."""
        with patch("chatGPTMidJourneyPrompt.chatbots.minimax.OpenAI"):
            bot = ChatbotMiniMax(api_key="test-key", temperature=0.0)
        assert bot.temperature == pytest.approx(0.01)

    def test_temperature_clamped_to_max(self):
        with patch("chatGPTMidJourneyPrompt.chatbots.minimax.OpenAI"):
            bot = ChatbotMiniMax(api_key="test-key", temperature=2.0)
        assert bot.temperature == pytest.approx(1.0)

    def test_temperature_valid_range(self):
        with patch("chatGPTMidJourneyPrompt.chatbots.minimax.OpenAI"):
            bot = ChatbotMiniMax(api_key="test-key", temperature=0.5)
        assert bot.temperature == pytest.approx(0.5)


class TestChatbotMiniMaxAsk:
    def _bot(self, **kwargs):
        with patch("chatGPTMidJourneyPrompt.chatbots.minimax.OpenAI"):
            bot = ChatbotMiniMax(api_key="test-key", **kwargs)
        return bot

    def test_ask_returns_string(self):
        bot = self._bot()
        bot.client.chat.completions.create.return_value = _make_response("hello world")
        result = bot.ask("generate a prompt")
        assert result == "hello world"

    def test_ask_sends_correct_model(self):
        bot = self._bot(model="MiniMax-M2.7-highspeed")
        bot.client.chat.completions.create.return_value = _make_response("prompt")
        bot.ask("test")
        call_kwargs = bot.client.chat.completions.create.call_args[1]
        assert call_kwargs["model"] == "MiniMax-M2.7-highspeed"

    def test_ask_sends_user_message(self):
        bot = self._bot()
        bot.client.chat.completions.create.return_value = _make_response("ok")
        bot.ask("my input")
        call_kwargs = bot.client.chat.completions.create.call_args[1]
        assert call_kwargs["messages"] == [{"role": "user", "content": "my input"}]

    def test_ask_passes_temperature(self):
        bot = self._bot(temperature=0.4)
        bot.client.chat.completions.create.return_value = _make_response("ok")
        bot.ask("test")
        call_kwargs = bot.client.chat.completions.create.call_args[1]
        assert call_kwargs["temperature"] == pytest.approx(0.4)

    def test_ask_multiline_prompt(self):
        bot = self._bot()
        expected = "a scenic landscape::5, mountains::4 --v 5 --s 1000"
        bot.client.chat.completions.create.return_value = _make_response(expected)
        result = bot.ask("mountains\nat sunset")
        assert result == expected

    def test_ask_returns_exact_content(self):
        """Ensure no extra stripping is done at this layer."""
        bot = self._bot()
        raw = '"quoted response."'
        bot.client.chat.completions.create.return_value = _make_response(raw)
        result = bot.ask("anything")
        assert result == raw


class TestChatbotMiniMaxModels:
    @pytest.mark.parametrize("model", [
        "MiniMax-M2.7",
        "MiniMax-M2.7-highspeed",
        "MiniMax-M2.5",
        "MiniMax-M2.5-highspeed",
    ])
    def test_supported_models(self, model):
        with patch("chatGPTMidJourneyPrompt.chatbots.minimax.OpenAI"):
            bot = ChatbotMiniMax(api_key="test-key", model=model)
        assert bot.model == model
