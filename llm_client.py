import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os
from openai import OpenAI


def call_llm(prompt,functions):
    api_key = os.getenv("DASHSCOPE_API_KEY")
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"

    #建立大模型客户端
    client = OpenAI(
        api_key=api_key,
        base_url = base_url,
    )

    #配置
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    print("CALLING LLM")
    response=client.chat.completions.create(
        model = "qwen-plus",
        messages= messages,
        tools=functions,  # 提供可调用的函数定义
        # 可选参数
        temperature=1.0,
        max_tokens=1000,
        top_p=1.0
    )
    response_message=response.choices[0].message
    functions_to_call = []

    #检查模型是否希望调用工具
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            print(f"TOOL CALL: {tool_call}")
            # 提取函数名和参数
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            functions_to_call.append({"name":name,"args":args})

    return functions_to_call




server_params = StdioServerParameters(
    command="mcp", # Executable
    args=["run","server.py"],# Optional command line arguments
    env=None, # Optional environment variables
)

def convert_to_llm_tool(tool):
    tool_schema = {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": {
                "type": "object",
                "properties": tool.inputSchema["properties"]
            }
        }
    }

    return tool_schema

async def run():
    async with stdio_client(server_params) as (read,write):
        async with ClientSession(
            read,write
        ) as session:
            # Initialize the connection
            await  session.initialize()

            ##列出服务器功能
            # List available resources
            resources = await session.list_resources()
            print("LISTING RESOURCES")
            for resource in resources:
                print("Resource: ", resource)


            # List available tools
            functions = []
            tools = await session.list_tools()
            print("LISTING TOOLS")
            for tool in tools.tools:
                print("Tool: ", tool.name)
                print("Tool", tool.inputSchema["properties"])
                functions.append(convert_to_llm_tool(tool))
            print("function:",functions)

            # Read a resource
            print("READING RESOURCE")
            content, mime_type = await session.read_resource("greeting://hello")

            # Call a tool
            print("CALL TOOL")
            result = await session.call_tool("get_local_weather", arguments={"city": "北京"})
            print(result.content[0].text)

            #Call a tool by llm
            prompt = "乌鲁木qi今天天气怎么样？"
            functions_to_call =call_llm(prompt,functions)
            for f in functions_to_call:
                result = await session.call_tool(f["name"],arguments=f["args"])
                print("Tool by llm result:",result.content[0].text)





if __name__ == "__main__" :
    import asyncio
    asyncio.run(run())