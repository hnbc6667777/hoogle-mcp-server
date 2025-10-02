# Hoogle MCP Server

一个 Model Context Protocol (MCP) 服务器，用于查询 Hoogle (Haskell API 搜索引擎)。

## 功能特性

- 🔍 搜索 Haskell 函数和类型
- 📚 获取详细的函数信息
- 🚀 快速的异步请求
- 📖 结构化的结果返回

## 安装

1. 克隆仓库：
```bash
git clone <repository-url>
cd hoogle-mcp-server
# hoogle-mcp-server

## 使用

复制以下配置：

``` json
{
  "mcpServers": {
    "hoogle": {
      "command": "uv",
      "args": [
        "--directory",
        "（你的仓库路径）",
        "run",
        "main.py"
      ]
    }
  }
}


```