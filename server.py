# server.py
from mcp.server.fastmcp import FastMCP
import requests
from typing import Optional

# Create an MCP server
mcp = FastMCP("Demo")

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


@mcp.tool()
def get_local_weather(city: str) -> str:
    """
    获取中国指定城市的实时天气情况
    :param city: 中国城市名称（如"北京"、"上海"）
    :return: 格式化的天气信息字符串
    """
    # 从环境变量获取API密钥
    import os
    api_key = os.environ.get("TIANAPI_KEY")
    if not api_key:
        return "错误：未设置API密钥，请设置TIANAPI_KEY环境变量"

    # 构建请求URL
    url = f"https://apis.tianapi.com/tianqi/index?key={api_key}&city={city}&type=1"

    try:
        # 发送请求
        response = requests.get(url)
        data = response.json()

        # 检查响应状态
        if data['code'] != 200:
            return f"获取天气信息失败：{data['msg']}"

        # 提取并格式化天气信息
        result = data['result']
        weather_info = f"""
        {result['area']}天气信息（{result['date']} {result['week']}）:
        天气：{result['weather']}
        温度：{result['real']}（最低{result['lowest']}，最高{result['highest']}）
        湿度：{result['humidity']}
        风向：{result['wind']} {result['windsc']}
        空气质量：{result['aqi']} - {result['quality']}
        """
        return weather_info

    except Exception as e:
        return f"获取天气信息时出错：{str(e)}"


# Main execution block - this is required to run the server
if __name__ == "__main__":
    mcp.run()