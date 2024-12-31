# Language Mentor Docker 部署文档

## 项目 Docker 结构

```
LanguageMentor/
├── Dockerfile              # Docker 镜像构建文件
├── docker-compose.yml      # Docker Compose 配置文件
├── .dockerignore          # Docker 忽略文件
└── scripts/               # Docker 相关脚本
    ├── docker-build.bat   # 构建镜像脚本
    ├── docker-run.bat     # 运行应用脚本
    └── docker-test.bat    # 运行测试脚本
```

## 配置文件说明

### Dockerfile
```dockerfile
# 使用Python 3.8作为基础镜像
FROM python:3.8-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY requirements.txt requirements-dev.txt ./
COPY src/ ./src/
COPY tests/ ./tests/
COPY scripts/ ./scripts/
COPY pytest.ini ./

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r requirements-dev.txt

# 暴露端口
EXPOSE 7860

# 设置启动命令
CMD ["python", "src/main.py"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  app:
    build: .
    container_name: language-mentor
    ports:
      - "7860:7860"
    volumes:
      - ./logs:/app/logs
      - ./htmlcov:/app/htmlcov
    environment:
      - GRADIO_SERVER_NAME=0.0.0.0
      - GRADIO_SERVER_PORT=7860
    command: python src/main.py

  test:
    build: .
    container_name: language-mentor-test
    volumes:
      - ./logs:/app/logs
      - ./htmlcov:/app/htmlcov
    command: python -m pytest tests/unit tests/integration --cov=src --cov-report=html --cov-report=term-missing
```

## 部署脚本

### scripts/docker-build.bat
```batch
@echo off
REM 构建Docker镜像
docker build -t language-mentor .
```

### scripts/docker-run.bat
```batch
@echo off
REM 运行应用容器
docker-compose up app
```

### scripts/docker-test.bat
```batch
@echo off
REM 运行测试容器
docker-compose up test
```

## 部署步骤

1. 构建 Docker 镜像：
```bash
scripts\docker-build.bat
```

2. 运行应用：
```bash
scripts\docker-run.bat
```

3. 运行测试：
```bash
scripts\docker-test.bat
```

4. 停止服务：
```bash
docker-compose down
```

## 访问服务

- 应用访问地址：http://localhost:7860
- 测试覆盖率报告：http://localhost:7860/htmlcov/

## 目录挂载

- 日志目录：`./logs:/app/logs`
- 测试覆盖率报告：`./htmlcov:/app/htmlcov`

## 环境变量

- GRADIO_SERVER_NAME=0.0.0.0
- GRADIO_SERVER_PORT=7860

## 注意事项

1. 确保已安装 Docker 和 Docker Compose
2. 确保 7860 端口未被占用
3. Windows 环境下使用 .bat 脚本
4. 日志和覆盖率报告会保存在本地目录
5. 容器内外端口映射为 7860:7860
6. 使用 volumes 持久化数据

## 常见问题

1. 端口冲突：
   - 修改 docker-compose.yml 中的端口映射

2. 权限问题：
   - 确保当前用户有 Docker 操作权限
   - 检查目录访问权限

3. 镜像构建失败：
   - 检查网络连接
   - 查看 Docker 日志
   - 确认依赖包版本兼容性

4. 容器启动失败：
   - 检查端口占用
   - 查看容器日志
   - 确认环境变量设置

## 维护建议

1. 定期更新基础镜像
2. 监控容器资源使用
3. 备份重要数据
4. 保持日志目录清理
5. 定期运行测试确保稳定性 