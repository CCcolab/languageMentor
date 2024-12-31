import pytest
from unittest.mock import patch, MagicMock
from src.tabs.scenario_tab import create_scenario_tab

class TestScenarioTab:
    @patch('gradio.Tab')
    def test_create_scenario_tab(self, mock_tab):
        # 设置模拟对象
        mock_tab_instance = MagicMock()
        mock_tab.return_value.__enter__.return_value = mock_tab_instance
        
        # 执行函数
        create_scenario_tab()
        
        # 验证是否创建了Tab
        mock_tab.assert_called_once_with("场景练习") 