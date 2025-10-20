from mcp.server.fastmcp import FastMCP
import asyncio

mcp = FastMCP(name="weather-demo", host="0.0.0.0", port=1234)

@mcp.tool(name="get_weather", description="获取指定城市的天气信息")
async def get_weather(city: str) -> str:
    weather_data = {
        "北京": "北京：晴，25°C",
        "上海": "上海：多云，27°C"
    }
    return weather_data.get(city, f"{city}：天气信息未知")

async def main():
    print("✅ 启动 MCP Server: <http://127.0.0.1:1234>")
    await mcp.run_sse_async()

if __name__ == "__main__":
    asyncio.run(main())