# 导入所需的模块和类
from langchain_ollama.chat_models import ChatOllama  # 导入 ChatOllama 模型
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # 导入提示模板相关类
from langchain_core.messages import HumanMessage  # 导入人类消息类
from utils.logger import LOG  # 导入日志工具

from langchain_core.chat_history import (
    BaseChatMessageHistory,  # 基础聊天消息历史类
    InMemoryChatMessageHistory,  # 内存中的聊天消息历史类
)
from langchain_core.runnables.history import RunnableWithMessageHistory  # 导入带有消息历史的可运行类

# 用于存储会话历史的字典
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """
    获取指定会话ID的聊天历史。如果该会话ID不存在，则创建一个新的聊天历史实例。
    
    参数:
        session_id (str): 会话的唯一标识符
    
    返回:
        BaseChatMessageHistory: 对应会话的聊天历史对象
    """
    if session_id not in store:
        # 如果会话ID不存在于存储中，创建一个新的内存聊天历史实例
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

class ConversationAgent:
    """
    对话代理类，负责处理与用户的对话。
    """
    def __init__(self):
        self.name = "Conversation Agent"  # 代理名称
        
        # 读取系统提示语，从文件中加载
        with open("prompts/conversation_prompt.txt", "r", encoding="utf-8") as file:
            self.system_prompt = file.read().strip()

        # 创建聊天提示模板，包括系统提示和消息占位符
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),  # 系统提示部分
            MessagesPlaceholder(variable_name="messages"),  # 消息占位符
        ])

        # 初始化 ChatOllama 模型，配置模型参数
        self.chatbot = self.prompt | ChatOllama(
            model="llama3.1:8b-instruct-q8_0",  # 使用的模型名称
            max_tokens=8192,  # 最大生成的token数
            temperature=0.8,  # 生成文本的随机性
        )

        # 将聊天机器人与消息历史记录关联起来
        self.chatbot_with_history = RunnableWithMessageHistory(self.chatbot, get_session_history)

        # 配置字典，包含会话ID等可配置参数
        self.config = {"configurable": {"session_id": "abc123"}}

    def chat(self, user_input):
        """
        处理用户输入并生成回复。
        
        参数:
            user_input (str): 用户输入的消息
        
        返回:
            str: 代理生成的回复内容
        """
        try:
            response = self.chatbot.invoke(
                [HumanMessage(content=user_input)],
            )
            return response.content
        except Exception as e:
            LOG.error(f"Error in chat: {e}")
            return "对不起，我无法处理您的请求。"

    def chat_with_history(self, user_input, chat_history=None):
        """
        处理用户输入并生成包含聊天历史的回复，同时记录日志。
        
        参数:
            user_input (str): 用户输入的消息
            chat_history (list): 聊天历史记录
        
        返回:
            tuple: (代理生成的回复内容, 例句列表)
        """
        # 调用 generate_response 方法并传递聊天历史
        bot_message = self.generate_response(user_input, chat_history)
        examples = self.generate_examples(user_input)  # 生成例句
        LOG.debug(bot_message)  # 记录调试日志
        return bot_message, examples  # 返回生成的回复内容和例句

    def generate_examples(self, user_input):
        # 这里可以根据用户输入生成例句
        # 示例：返回固定的例句，实际应用中可以根据上下文生成
        return [
            "What are your thoughts on this topic?",
            "Can you provide an example to illustrate your point?",
            "How do you feel about the current situation?"
        ]

    def generate_response(self, user_input, chat_history):
        """
        生成 Bot 的回复逻辑，结合用户输入和聊天历史。
        
        参数:
            user_input (str): 用户输入的消息
            chat_history (list): 聊天历史记录
        
        返回:
            str: 代理生成的回复内容
        """
        LOG.debug(f"Generating response for user input: {user_input} with history: {chat_history}")
        # 将用户输入和聊天历史结合起来
        messages = chat_history or []
        messages.append(HumanMessage(content=user_input))  # 添加用户输入到消息列表

        # 使用聊天模型生成回复
        response = self.chatbot.invoke(messages)
        return response.content  # 返回生成的回复内容
