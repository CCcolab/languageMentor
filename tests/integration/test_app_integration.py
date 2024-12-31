import pytest
from gradio.test_utils import GradioTestClient
from src.main import language_mentor_app

class TestAppIntegration:
    @pytest.fixture
    def client(self):
        return GradioTestClient(language_mentor_app)
    
    def test_app_loads(self, client):
        # 测试应用是否成功加载
        response = client.get("/")
        assert response.status_code == 200 