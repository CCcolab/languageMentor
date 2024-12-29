# LanguageMentor

LanguageMentor 是一个基于 Langchain 和 Chatbot 的在线英语自助学习平台，旨在帮助用户通过对话练习和场景训练提高英语水平。

## 特性

- **对话练习**：与智能聊天机器人进行对话，获取实时反馈。
- **场景训练**：选择不同的场景（如求职面试、酒店入住、薪资谈判等）进行针对性练习。
- **教学点评**：每次对话后，系统会提供教学点评和例句，帮助用户更好地理解和应用所学内容。

## 技术栈

- Python
- Gradio
- Langchain
- Ollama
- unittest

## 安装

1. 克隆项目：

   ```bash
   git clone https://github.com/yourusername/LanguageMentor.git
   cd LanguageMentor
   ```

2. 创建并激活虚拟环境：

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # macOS/Linux
   ```

3. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

## 使用

1. 启动应用：

   ```bash
   python src/main.py
   ```

2. 打开浏览器，访问 `http://localhost:7860` 以使用应用。

## 运行测试

在项目根目录下，您可以运行以下命令来执行测试：
