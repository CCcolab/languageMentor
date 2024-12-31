@echo off
REM 激活 conda 环境
call conda activate lm

REM 检查是否需要安装依赖
pip list | findstr pytest >nul
if errorlevel 1 (
    echo Installing development dependencies...
    pip install -r requirements-dev.txt
)

REM 运行测试
scripts\run_tests.bat

REM 等待用户按键后退出
pause 