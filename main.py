import requests
from bs4 import BeautifulSoup

def simple_hoogle_parser(query):
    """
    简化版的Hoogle搜索和解析
    """
    url = "https://hoogle.haskell.org/"
    
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i'
    }
    
    response = requests.get(url, headers=headers, params={'hoogle': query})
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
                    'doc': doc[:100] + "..." if len(doc) > 100 else doc,  # 限制长度
                    'url': url
                })
    
    return results

# 使用示例
if __name__ == "__main__":
    results = simple_hoogle_parser("map")
    
    print(f"找到 {len(results)} 个结果:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['name']}")
        if result['signature']:
            print(f"   类型: {result['signature']}")
        if result['doc']:
            print(f"   文档: {result['doc']}")
        print(f"   链接: {result['url']}")
