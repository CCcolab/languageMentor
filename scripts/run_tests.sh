#!/bin/bash

# 安装开发依赖
pip install -r requirements-dev.txt

# 运行单元测试并生成覆盖率报告
pytest tests/unit --cov=src --cov-report=html --cov-report=term-missing

# 运行集成测试
pytest tests/integration

# 检查覆盖率是否达到80%
coverage report --fail-under=80 