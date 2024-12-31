import pytest
import gradio as gr
from src.main import main
from unittest.mock import patch, MagicMock

class TestMain:
    @patch('gradio.Blocks')
    @patch('src.tabs.scenario_tab.create_scenario_tab')
    @patch('src.tabs.conversation_tab.create_conversation_tab')
    @patch('src.tabs.vocab_tab.create_vocab_tab')
    def test_main_creates_app(self, mock_vocab_tab, mock_conv_tab, 
                            mock_scenario_tab, mock_blocks):
        # 设置模拟对象
        mock_app = MagicMock()
        mock_blocks.return_value.__enter__.return_value = mock_app
        
        # 执行主函数
        main()
        
        # 验证是否调用了所有必要的函数
        mock_blocks.assert_called_once()
        mock_scenario_tab.assert_called_once()
        mock_conv_tab.assert_called_once()
        mock_vocab_tab.assert_called_once()
        mock_app.launch.assert_called_once_with(share=True, server_name="0.0.0.0") 