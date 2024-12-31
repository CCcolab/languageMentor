# Language Mentor 测试框架文档

## 项目测试结构
ash
LanguageMentor/
├── tests/ # 测试目录
│ ├── unit/ # 单元测试
│ │ ├── init.py
│ │ ├── test_main.py # 主程序测试
│ │ ├── test_scenario_tab.py
│ │ ├── test_conversation_tab.py
│ │ ├── test_vocab_tab.py
│ │ └── test_logger.py
│ └── integration/ # 集成测试
│ ├── init.py
│ ├── test_app_integration.py
│ └── test_workflow.py
├── scripts/ # 脚本目录
│ ├── run_tests.bat # 运行测试脚本
│ └── view_coverage.bat # 查看覆盖率报告脚本
├── logs/ # 日志目录
├── htmlcov/ # 覆盖率报告目录
├── pytest.ini # pytest 配置文件
└── requirements-dev.txt # 测试依赖配置

## 配置文件

### pytest.ini
ini
[pytest]
testpaths = tests
python_files = test_.py
python_classes = Test
python_functions = test_
addopts = -v --cov=src --cov-report=html --cov-report=term-missing


### requirements-dev.txt
text
pytest>=7.4.3
pytest-cov>=4.1.0
pytest-mock>=3.12.0
coverage>=7.3.2


## 测试脚本

### scripts/run_tests.bat
batch
@echo off
REM 激活 conda 环境
call conda activate lm
REM 切换到项目根目录
cd /d %~dp0\..
REM 创建logs目录（如果不存在）
if not exist logs mkdir logs
REM 安装所有必要的测试依赖
pip install pytest pytest-cov coverage -r requirements-dev.txt > logs/pip_install.log 2>&1
REM 运行测试并保存输出
(
echo Test run started at: %date% %time%
echo.
REM 运行单元测试并生成覆盖率报告
python -m pytest tests/unit --cov=src --cov-report=html --cov-report=term-missing
echo.
echo Integration tests:
python -m pytest tests/integration
echo.
echo Coverage report:
python -m coverage report --fail-under=80
) > logs/test_results.log 2>&1
REM 在控制台显示结果
type logs\test_results.log
REM 保持窗口打开以查看结果
pause


### scripts/view_coverage.bat
batch
@echo off
REM 激活 conda 环境
call conda activate lm
REM 切换到项目根目录
cd /d %~dp0\..
REM 检查是否安装了 http.server
python -c "import http.server" 2>nul
if errorlevel 1 (
echo Installing http.server...
pip install http.server
)
REM 启动简单的 HTTP 服务器在 8000 端口
echo 正在启动覆盖率报告服务器...
echo 请在浏览器中访问: http://localhost:8000/htmlcov/
echo 按 Ctrl+C 停止服务器
python -m http.server 8000


## 单元测试

### tests/unit/test_main.py
python
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
mock_blocks.return_value.enter.return_value = mock_app
# 执行主函数
main()
# 验证是否调用了所有必要的函数
mock_blocks.assert_called_once()
mock_scenario_tab.assert_called_once()
mock_conv_tab.assert_called_once()
mock_vocab_tab.assert_called_once()
mock_app.launch.assert_called_once_with(share=True, server_name="0.0.0.0")


### tests/unit/test_scenario_tab.py
python
import pytest
from unittest.mock import patch, MagicMock
from src.tabs.scenario_tab import create_scenario_tab
class TestScenarioTab:
@patch('gradio.Tab')
def test_create_scenario_tab(self, mock_tab):
# 设置模拟对象
mock_tab_instance = MagicMock()
mock_tab.return_value.enter.return_value = mock_tab_instance
# 执行函数
create_scenario_tab()
# 验证是否创建了Tab
mock_tab.assert_called_once_with("场景练习")


### tests/unit/test_conversation_tab.py
python
import pytest
from unittest.mock import patch, MagicMock
from src.tabs.conversation_tab import create_conversation_tab
class TestConversationTab:
@patch('gradio.Tab')
def test_create_conversation_tab(self, mock_tab):
mock_tab_instance = MagicMock()
mock_tab.return_value.enter.return_value = mock_tab_instance
create_conversation_tab()
mock_tab.assert_called_once_with("对话练习")


### tests/unit/test_vocab_tab.py
python
import pytest
from unittest.mock import patch, MagicMock
from src.tabs.vocab_tab import create_vocab_tab
class TestVocabTab:
@patch('gradio.Tab')
def test_create_vocab_tab(self, mock_tab):
mock_tab_instance = MagicMock()
mock_tab.return_value.enter.return_value = mock_tab_instance
create_vocab_tab()
mock_tab.assert_called_once_with("词汇学习")


### tests/unit/test_logger.py
python
import pytest
from src.utils.logger import LOG
class TestLogger:
def test_logger_info(self, caplog):
test_message = "Test log message"
LOG.info(test_message)
assert test_message in caplog.text


## 集成测试

### tests/integration/test_app_integration.py
python
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


### tests/integration/test_workflow.py
python
import pytest
from gradio.test_utils import GradioTestClient
from src.main import language_mentor_app
class TestWorkflow:
@pytest.fixture
def client(self):
return GradioTestClient(language_mentor_app)
def test_scenario_workflow(self, client):
# 测试场景练习工作流
response = client.submit(
fn_index=0, # 场景选择函数的索引
inputs=["商务会议"] # 测试输入
)
assert response is not None
def test_conversation_workflow(self, client):
# 测试对话练习工作流
response = client.submit(
fn_index=1, # 对话函数的索引
inputs=["Hello"]
)
assert response is not None


## 使用说明

1. 环境准备：
bash
确保在 conda 环境中
conda activate lm
安装测试依赖
pip install -r requirements-dev.txt

2. 运行测试：
bash
方式1：使用批处理脚本
scripts\run_tests.bat
方式2：直接使用 pytest
python -m pytest tests/unit --cov=src --cov-report=html --cov-report=term-missing
python -m pytest tests/integration

3. 查看测试结果：
- 命令行输出：直接查看终端
- 日志文件：查看 `logs/test_results.log`
- 覆盖率报告：
  ```bash
  scripts\view_coverage.bat
  ```
  然后访问 http://localhost:8000/htmlcov/

## 注意事项

1. 确保所有测试文件名以 `test_` 开头
2. 所有测试类名以 `Test` 开头
3. 所有测试方法名以 `test_` 开头
4. 保持测试覆盖率在 80% 以上
5. 定期运行测试并检查覆盖率报告
6. 添加新功能时同步添加相应的测试用例

