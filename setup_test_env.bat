@echo off
REM 激活 conda 环境
call conda activate lm

REM 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

REM 创建测试目录结构
if not exist tests\unit mkdir tests\unit
if not exist tests\integration mkdir tests\integration
if not exist tests\__init__.py type nul > tests\__init__.py
if not exist tests\unit\__init__.py type nul > tests\unit\__init__.py
if not exist tests\integration\__init__.py type nul > tests\integration\__init__.py

echo Test environment setup complete!
pause 