# coding=utf-8
# @Author: Fulai Cui (cuifulai@mail.hfut.edu.cn)
# @Time: 2022/3/11 20:29
import requests
from bs4 import BeautifulSoup
import re
import json


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

        #
        header = html.findAll('div', attrs={'class': 'wp_header'})[0]

        # 作品
        musics = {}
        divs = html.findAll('div', attrs={'lang': 'zh', 'dir': 'ltr'})
        for div in divs:
            script = div.findAll('script')[1]
            p = re.findall(r'catpagejs,(.+?)\);if', str(script))[0]
            p = json.loads(p)

            for index in p:
                musics[index] = p[index]
        info['production'] = musics

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
        f.write(json.dumps(musics))


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

    crawler = Crawler("https://cn.imslp.org/wiki/" + music, '../Data/Music/Abbé_Stadler,_WoO_178_(Beethoven,_Ludwig_van).html')
    crawler.set_html()
    # crawler.get_html()
    info = crawler.parse()

    save(info, '../Data/Result/Music/' + music + '.json')

    statistic(info['production'])


if __name__ == '__main__':
    main()
