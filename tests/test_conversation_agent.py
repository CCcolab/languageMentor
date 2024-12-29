import unittest
from agents.conversation_agent import ConversationAgent

class TestConversationAgent(unittest.TestCase):
    def setUp(self):
        self.agent = ConversationAgent()

    def test_chat(self):
        response = self.agent.chat("Hello, how are you?")
        self.assertIsInstance(response, str)  # 确保返回的是字符串

    def test_generate_examples(self):
        examples = self.agent.generate_examples("Tell me something.")
        self.assertEqual(len(examples), 3)  # 确保返回三个例句

if __name__ == "__main__":
    unittest.main() 