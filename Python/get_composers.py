# coding=utf-8
# @Author: Fulai Cui (cuifulai@mail.hfut.edu.cn)
# @Time: 2022/3/8 20:29
import requests
from bs4 import BeautifulSoup
import re
import json


Headers = {
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
}


class Crawler:
    def __init__(self, url, file):
        self.URL = url
        self.File = file

        self.HTML = None

    def set_html(self):
        html = requests.get(self.URL, headers=Headers)
        self.HTML = html.text

        with open(self.File, 'w', encoding='utf-8') as f:
            print(self.HTML, file=f)

    def get_html(self):
        with open(self.File, 'r', encoding='utf-8') as f:
            self.HTML = f.read()

    def parse(self):
        html = BeautifulSoup(self.HTML, 'lxml')

        # <div lang="zh" dir="ltr">
        div = html.findAll('div', attrs={'lang': 'zh', 'dir': 'ltr'})[0]
        script = div.script
        s1 = re.findall(r'catpagejs,(.+?)\);if', str(script))[0]

        return json.loads(s1)


def save(composers, file):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(composers))


def statistic(composers):
    counts = {}

    print(len(composers))

    num = 0
    for index in composers:
        counts[index] = len(composers[index])
        num += len(composers[index])
    print(counts)
    print(len(counts))
    print(num)


def main():
    category = 'Composers'

    crawler = Crawler("https://cn.imslp.org/wiki/Category:" + category, '../Data/composers.html')
    # composers.set_html()
    crawler.get_html()
    composers = crawler.parse()

    # save(composers, '../Data/Result/composers.json')

    statistic(composers['s1'])


if __name__ == '__main__':
    main()
