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