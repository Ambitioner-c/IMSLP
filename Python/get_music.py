# coding=utf-8
# @Author: Fulai Cui (cuifulai@mail.hfut.edu.cn)
# @Time: 2022/3/11 20:29
import requests
from bs4 import BeautifulSoup
import re
import json
from time import sleep
from random import randint


Headers = {
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
        info = {}

        html = BeautifulSoup(self.HTML, 'lxml')

        # 头部
        header = html.findAll('div', attrs={'class': 'wp_header'})[0]

        # 作品
        musics = {}
        divs = html.findAll('div', attrs={'class': re.compile(r'we_fileblock_2')})

        prefs = []
        for div in divs:
            imslp_id = re.findall(r'id="IMSLP(.+?)"', str(div))[0]

            url = 'https://cn.imslp.org/wiki/Special:IMSLPDisclaimerAccept/' + str(imslp_id)
            _html = requests.get(url, headers=Headers)
            _html = _html.text
            pref = re.findall(r'data-id="(.+?)"', str(_html))[0].replace('&#58;', ':')
            prefs.append(pref)

            sleep(randint(1, 3))

        info['prefs'] = prefs

        # 分类
        categories = []
        ul = html.findAll('div', attrs={'id': 'mw-normal-catlinks'})[0].ul
        for a in ul.findAll('a'):
            categories.append(a.text)
        info['category'] = categories

        # 浏览量
        footer = html.findAll('footer')[0]
        times = re.findall(r'>(.+?) times', str(footer))[0]
        info['times'] = times

        return info


def save(musics, file):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(musics, ensure_ascii=False))


def statistic(musics):
    counts = {}

    print(len(musics))

    num = 0
    for _ in musics:
        for __ in musics[_]:
            counts[_ + __] = len(musics[_][__])
            num += len(musics[_][__])
    print(counts)
    print(len(counts))
    print(num)


def main():
    music = 'Abbé_Stadler,_WoO_178_(Beethoven,_Ludwig_van)'

    crawler = Crawler("https://cn.imslp.org/wiki/" + music, '../Data/Music/' + music + '.html')
    crawler.set_html()
    # crawler.get_html()
    info = crawler.parse()

    save(info, '../Data/Result/Music/' + music + '.json')

    statistic(info['prefs'])


if __name__ == '__main__':
    main()

