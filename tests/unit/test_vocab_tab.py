import pytest
from unittest.mock import patch, MagicMock
from src.tabs.vocab_tab import create_vocab_tab

class TestVocabTab:
    @patch('gradio.Tab')
    def test_create_vocab_tab(self, mock_tab):
        mock_tab_instance = MagicMock()
        mock_tab.return_value.__enter__.return_value = mock_tab_instance
        
        create_vocab_tab()
        
        mock_tab.assert_called_once_with("词汇学习") 