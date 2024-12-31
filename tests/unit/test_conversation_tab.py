import pytest
from unittest.mock import patch, MagicMock
from src.tabs.conversation_tab import create_conversation_tab

class TestConversationTab:
    @patch('gradio.Tab')
    def test_create_conversation_tab(self, mock_tab):
        mock_tab_instance = MagicMock()
        mock_tab.return_value.__enter__.return_value = mock_tab_instance
        
        create_conversation_tab()
        
        mock_tab.assert_called_once_with("对话练习") 