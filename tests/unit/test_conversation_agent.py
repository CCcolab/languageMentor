import pytest
from unittest.mock import patch, MagicMock
from src.agents.conversation_agent import ConversationAgent

class TestConversationAgent:
    @pytest.fixture
    def agent(self):
        return ConversationAgent()
    
    @patch('openai.ChatCompletion.create')
    def test_generate_response(self, mock_create, agent):
        mock_create.return_value = {
            'choices': [{'message': {'content': 'Test response'}}]
        }
        
        response = agent.generate_response("Test prompt")
        
        assert response == "Test response"
        mock_create.assert_called_once() 