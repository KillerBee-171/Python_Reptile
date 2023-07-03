import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm

def get_novel_chapters():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }

    root_url = "https://www.xxbiqudu.com/146_146621/"
    r = requests.get(root_url, headers=headers)
    r.encoding = "gbk"
    soup = BeautifulSoup(r.text, "html.parser")

    data = []
    for dd in soup.find_all("dd"):
        link = dd.find("a")
        if not link:
            continue
        data.append((link["href"], link.get_text()))
    return data

def get_chapters_content(url):
    r = requests.get(url)
    r.encoding = "gbk"
    soup = BeautifulSoup(r.text, "html.parser")
    content_div = soup.find("div", id="content")
    content = content_div.get_text("\n")
    content = re.sub(r"\n+", "\n", content)
    return content.strip()

chapters_list = get_novel_chapters()

for index, chapters in enumerate(tqdm(chapters_list)):
    url, title = chapters
    content = get_chapters_content(url)

    # 对标题进行处理，去除特殊字符并添加序号
    title = re.sub(r'[\/:*?"<>|]', '', title)
    filename = f"{index+1:03d}_{title}.txt"  # 添加序号并格式化文件名

    with open(f"/Users/echo/Documents/道诡异仙/{filename}", "w", encoding="utf-8") as fout:
        fout.write(content)
