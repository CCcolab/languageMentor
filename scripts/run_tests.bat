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