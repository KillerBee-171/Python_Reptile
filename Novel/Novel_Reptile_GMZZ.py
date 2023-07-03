import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm


def get_novel_chapters():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }

    root_url = "https://www.biquge365.net/newbook/65301/"
    r = requests.get(root_url, headers=headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, "html.parser")

    data = []
    all_title = soup.find_all("ul", attrs={"class": "info"})
    if all_title:
        for dd in all_title[0].find_all("li"):
            link = dd.find("a")
            if link:
                chapter_url = link.get("href")
                data.append(("https://www.biquge365.net%s" % link['href'], link.get_text()))
        return data
    else:
        print("No title found.")


def get_chapter_content(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, "html.parser")
    content_div = soup.find("div", id="txt")

    # 删除第一行广告
    ad_tag = content_div.find_all("p")[0]
    if ad_tag:
        ad_tag.decompose()

    # 获取章节内容
    content = "\n".join(content_div.stripped_strings)
    return content


def crawl_novel():
    chapters = get_novel_chapters()
    total_chapters = len(chapters)
    base_dir = "/Users/echo/Documents/诡秘之主"
    time.sleep(2)  # 延迟2秒开始爬取，限制爬取频率

    with tqdm(total=total_chapters, ncols=80, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
        for i, chapter in enumerate(chapters):
            url, title = chapter
            content = get_chapter_content(url)

            file_path = f"{base_dir}/{i + 1}. {title}.txt"
            with open(file_path, "w", encoding="utf-8") as fout:
                fout.write(content)

            pbar.set_postfix({"Chapter": i + 1, "Title": title})
            pbar.update(1)
            time.sleep(1)  # 延迟1秒继续下一章节的爬取，限制爬取频率


crawl_novel()
