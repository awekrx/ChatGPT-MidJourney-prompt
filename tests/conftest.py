"""Mock revChatGPT so tests run without the package installed."""
import sys
from unittest.mock import MagicMock

# Provide stub modules for revChatGPT which is not required to run MiniMax tests
_revchatgpt = MagicMock()
_revchatgpt.V1.Chatbot = MagicMock
_revchatgpt.V3.Chatbot = MagicMock
sys.modules.setdefault("revChatGPT", _revchatgpt)
sys.modules.setdefault("revChatGPT.V1", _revchatgpt.V1)
sys.modules.setdefault("revChatGPT.V3", _revchatgpt.V3)
