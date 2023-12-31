import pytest
from app import StreamlitChatPack

def test_StreamlitChatPack_init():
    chat_pack = StreamlitChatPack(page="Test Page")
    assert chat_pack.page == "Test Page"