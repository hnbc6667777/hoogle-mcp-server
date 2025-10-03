from mcp.server.fastmcp import FastMCP
import requests
from bs4 import BeautifulSoup

# 创建 MCP 服务器实例
mcp = FastMCP("Hoogle Search Server")

@mcp.tool()
def hoogle_search(query: str) -> str:
    """
    在 Hoogle 上搜索 Haskell 函数和类型签名
    
    Args:
        query: 要搜索的 Haskell 函数名或类型签名
        
    Returns:
        str: 格式化后的搜索结果
    """
    url = "https://hoogle.haskell.org/"
    
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i'
    }
    
    try:
        response = requests.get(url, headers=headers, params={'hoogle': query})
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取所有结果
        results = []
        for div in soup.find_all('div', class_='result'):
            # 提取名称和链接
            ans_div = div.find('div', class_='ans')
            if ans_div:
                link = ans_div.find('a')
                if link:
                    name = link.get_text(strip=True)
                    url = link.get('href', '')
                    
                    # 提取类型签名（如果有）
                    signature = ""
                    if '::' in name:
                        signature = name
                        # 提取函数名
                        name_parts = name.split('::')
                        if len(name_parts) > 0:
                            name = name_parts[0].strip()
                    
                    # 提取文档
                    doc_div = div.find('div', class_='doc')
                    doc = doc_div.get_text(strip=True) if doc_div else ""
                    
                    results.append({
                        'name': name,
                        'signature': signature,
                        'doc': doc[:100] + "..." if len(doc) > 100 else doc,
                        'url': url
                    })
        
        # 格式化输出结果
        if not results:
            return f"在 Hoogle 上搜索 '{query}' 未找到结果"
        
        output = [f"在 Hoogle 上搜索 '{query}' 找到 {len(results)} 个结果:\n"]
        
        for i, result in enumerate(results, 1):
            output.append(f"{i}. {result['name']}")
            if result['signature']:
                output.append(f"   类型: {result['signature']}")
            if result['doc']:
                output.append(f"   文档: {result['doc']}")
            if result['url']:
                # 确保 URL 是完整的
                full_url = result['url']
                if not full_url.startswith('http'):
                    full_url = 'https://hoogle.haskell.org' + full_url
                output.append(f"   链接: {full_url}")
            output.append("")  # 空行分隔
        
        return "\n".join(output)
        
    except Exception as e:
        return f"搜索过程中出现错误: {str(e)}"

def main():
    """主函数入口"""
    mcp.run(transport="stdio")

# 运行服务器
if __name__ == "__main__":
    main()