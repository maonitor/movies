from lxml import etree
import requests

BASE_URL = 'https://www.dytt8.net'
HEADERS= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/80.0.3987.100 Safari/537.36',
          'Referer': 'https://www.dytt8.net/html/gndy/dyzz/index.html'}
def get_detail_urls(url):
    resp = requests.get(url, headers=HEADERS)
    text = resp.content.decode(encoding='gbk', errors='ignore')
    html = etree.HTML(text)
    detail_urls = html.xpath("//table[@class='tbspan']//a/@href")
    detail_urls = map(lambda url: BASE_URL+url, detail_urls)
    return detail_urls

def parse_detail_page(url):
    resp = requests.get(url, headers=HEADERS)
    text = resp.content.decode(encoding='gbk', errors='ignore')
    html = etree.HTML(text)
    title = html.xpath("//div[@class='title_all']//font[@color='#07519a']/text()")
    pic = html.xpath("//div[@id='Zoom']//img[@border='0']/@src")
    infos = html.xpath("//div[@id='Zoom']//text()")
    download = html.xpath("//div[@id='Zoom']//a/@href")
    movie = {'title': title[0],
             'pic': pic[0],
             'year': infos[5][6:],
             'language': infos[8][6:],
             'size': infos[15][6:],
             'length': infos[16][6:],
             'download': download[0]}
    return movie

def spider():
    base_url = 'https://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'
    with open('movies.txt', 'w', encoding='utf-8') as fp:
        for x in range(1, 3):
            url = base_url.format(x)
            detail_urls = get_detail_urls(url)
            for detail_url in detail_urls:
                i = parse_detail_page(detail_url)
                for a in i:
                    print(i[a])
                    fp.write(a + ':' + i[a])
                    fp.write('\n')
                fp.write('\n')

if __name__ == '__main__':
    spider()