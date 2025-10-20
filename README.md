# MCP-LLM 演示项目

这是一个基于 MCP (Model-Client-Protocol) 和大语言模型的演示项目，展示了如何构建一个具有工具调用能力的 LLM 应用服务。

## 项目概述

本项目通过 MCP 框架实现了一个服务端，提供了多种工具（如加法运算、天气查询等），并通过客户端调用大语言模型（支持 OpenAI 和阿里云 DashScope 接口）来解析用户请求并调用相应的工具。

## 项目结构

```
.
├── llm_client.py     # DashScope 接口调用客户端
├── server.py         # MCP 服务端，提供多种工具
├── stdio-server.py   # 基于标准输入输出的 MCP 服务端
├── test.py           # 简单的天气服务测试
├── requirements.txt  # 项目依赖
└── .gitignore        # Git 忽略文件
```

## 功能特性

1. **MCP 服务端功能**：
   - 提供加法运算工具
   - 提供个性化问候资源
   - 提供天气查询功能（基于天气 API）

2. **LLM 客户端功能**：
   - 支持调用 OpenAI 接口（Azure 和 DashScope 兼容模式）
   - 自动转换 MCP 工具为 LLM 可调用的函数格式
   - 处理工具调用结果

3. **示例服务器**：
   - 标准输入输出服务器
   - 流式输出服务器

## 安装与配置

### 环境要求

- Python 3.8+
- pip 包管理器

### 安装步骤

1. 克隆项目到本地

```bash
git clone <repository-url>
cd mcp-llm-demo
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 配置环境变量

创建 `.env` 文件或直接在系统中设置以下环境变量：

```
# 阿里云 DashScope API 密钥（用于调用 qwen-plus 模型）
DASHSCOPE_API_KEY=your_dashscope_api_key

# 天气 API 密钥
TIANAPI_KEY=your_tianapi_key

# Azure OpenAI 相关配置（可选）
GITHUB_TOKEN=your_azure_openai_token
```

## 使用方法

### 启动 MCP 服务端

```bash
python server.py
```

### 启动标准输入输出服务器

```bash
python stdio-server.py
```


### 运行 LLM 客户端

```bash
python llm_client.py
```

## 工具说明

### 加法工具 (`add`)

**功能**：计算两个数字的和

**参数**：
- `a` (int): 第一个数字
- `b` (int): 第二个数字

**返回值**：两个数字的和

### 天气查询工具 (`get_local_weather`)

**功能**：获取中国指定城市的实时天气情况

**参数**：
- `city` (str): 中国城市名称（如"北京"、"上海"）

**返回值**：格式化的天气信息字符串

### 问候资源 (`greeting://{name}`)

**功能**：获取个性化问候

**参数**：
- `name` (str): 要问候的人名

**返回值**：个性化的问候字符串

## 注意事项

1. 在使用天气查询功能前，请确保已设置有效的 `TIANAPI_KEY` 环境变量
2. 调用大语言模型前，需确保已设置相应的 API 密钥
3. 本项目仅作为演示用途，实际应用中请确保 API 密钥的安全管理

## 扩展开发

如需添加新的工具或资源，请在相应的服务端文件中使用 `@mcp.tool()` 或 `@mcp.resource()` 装饰器进行注册。

## 许可证

[MIT License](LICENSE)

## 联系方式

如有问题或建议，请提交 Issue 或 Pull Request。
