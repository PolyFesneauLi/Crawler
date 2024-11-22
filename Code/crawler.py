import requests
import re
from urllib import parse

exist_url = []
writeCount = 0
urls = []

def load(url):
    global writeCount
    req = requests.get(url)
    html = req.content.decode('utf-8')
    
    con = re.findall(r'(?<=href=")[^\"]+[^index].htm', html)
    for x in range(0, len(con)):
        url2 = con[x]
        url1 = 'https://'  # 解析网页中所有子URL
        # 将链接拼接
        newUrl = parse.urljoin(url1, url2)
        urls.append(newUrl)
    print(urls)
    # 去掉已爬取的链接和重复链接
    unique_list = list(set(urls) - set(exist_url))
    print(unique_list)

    # 将读取内容写入文件
    with open('./output_SDI/' + str(writeCount) + '.txt', 'w', encoding='utf-8') as fp:
        fp.write(req.text)
    writeCount += 1
    # 遍历所有子URL再次调用
    for i in range(0, len(unique_list)):
        load(unique_list[i])
    return

url = 'https://di.hkex.com.hk/di/NSSrchCorpList.aspx?sa1=cl&scsd=01/07/2023&sced=31/12/2023&sc=1477&src=MAIN&lang=EN&g_lang=en'
load(url)