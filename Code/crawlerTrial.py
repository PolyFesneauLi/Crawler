import requests
import pandas as pd
import os
from bs4 import BeautifulSoup

# 假设你已经有了 stock_code, company_name 和 report_links 列表
# 这里是一个示例，实际数据需要从你的爬虫代码中获取
stock_code = ["01477"]
company_name = ["Ocumension Therapeutics"]
report_links = [{
    "Complete list of substantial shareholders": "link1",
    "Consolidated list of substantial shareholders": "link2",
    "List of notices filed by substantial shareholders": "link3",
    "Complete list of directors": "link4",
    "List of notices filed by directors": "link5",
    "List of all notices": "link6",
}]

# 创建 DataFrame
data = {
    "Stock Code": stock_code,
    "Company Name": company_name,
    "Complete list of substantial shareholders": [link["Complete list of substantial shareholders"] for link in report_links],
    "Consolidated list of substantial shareholders": [link["Consolidated list of substantial shareholders"] for link in report_links],
    "List of notices filed by substantial shareholders": [link["List of notices filed by substantial shareholders"] for link in report_links],
    "Complete list of directors": [link["Complete list of directors"] for link in report_links],
    "List of notices filed by directors": [link["List of notices filed by directors"] for link in report_links],
    "List of all notices": [link["List of all notices"] for link in report_links],
}
df = pd.DataFrame(data)

# 创建保存 Excel 文件的目录
stock_name = "Ocumension Therapeutics"
stock_number = "01477"
directory = f'./output_SDI/{stock_name} ({stock_number})'
os.makedirs(directory, exist_ok=True)

# 保存总表到 Excel
output_file = f'{directory}/{stock_name} ({stock_number}).xlsx'
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Summary', index=False)

    # 访问每个子链接并提取表格数据
    for link_name, link_url in report_links[0].items():
        response = requests.get(link_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 假设每个子链接的表格数据可以用 pandas 读取
        # 这里需要根据实际情况解析表格数据
        tables = pd.read_html(str(soup))
        
        # 保存每个表格到一个新的工作表中
        for idx, table in enumerate(tables):
            sheet_name = f'{stock_name}_{link_name}_{idx + 1}'
            table.to_excel(writer, sheet_name=sheet_name, index=False)

print(f'Data saved to {output_file}')