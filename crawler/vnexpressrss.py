import requests
from bs4 import BeautifulSoup
from base import BaseClass
from common.check_file_empty import is_file_empty


class VNExpressRSS(BaseClass):
    def __init__(self):
        super().__init__()
        vnexpress_rss_url = 'https://vnexpress.net/rss'
        res = requests.get(vnexpress_rss_url).text
        self.soup = BeautifulSoup(res, 'lxml')

    def extract(self):
        self.log.info("Extracting RSS link...")
        rss_link_container = self.soup.find('div', attrs={'class': 'wrap-list-rss'})
        rss_link = rss_link_container.findAll('a')
        self.log.info("Finished extracting RSS link...")
        return ['https://vnexpress.net' + i.get('href') for i in rss_link]

    def load(self):
        self.log.info("Saving link...")
        rss_links = self.extract()
        with open('data/vnexpressrss_rss_link.txt', 'w+') as f:
            for link in rss_links:
                f.writelines(link + '\n')
            self.log.info("Successfully saved.")


class RssExtractor(BaseClass):
    def __init__(self):
        super().__init__()
        if is_file_empty('data/vnexpressrss_rss_link.txt'):
            VNExpressRSS().load()
        self.log.info('Getting rss links')
        with open('data/vnexpressrss_rss_link.txt', 'r') as f:
            self.link = [i[:-1] for i in f.readlines()]
            self.log.info('Successfully getting rss links')

    def _extractor(self, link):
        sublinks = []
        res = requests.get(link).text
        soup = BeautifulSoup(res, 'xml')
        for desc in soup.findAll('description'):
            for descchild in desc.children:
                descchild = descchild.split()
                for c in descchild:
                    if c.startswith('href="https://vnexpress.net'):
                        sublinks.append(c[6:-6])

        return sublinks

    def extract(self):
        newslink = []
        self.log.info("Extracting news url...")
        for url in self.link:
            newslink = newslink + self._extractor(url)
        self.log.info("Successfully extracted news url")
        return newslink

    def load(self):
        self.log.info("Saving link...")
        news_links = self.extract()
        with open('data/vnexpressrss_news_link.txt', 'w+') as f:
            for link in news_links:
                f.writelines(link + '\n')
            self.log.info("Successfully saved.")

class NewsExtractor(BaseClass):
    def __init__(self):
        super().__init__()
        if is_file_empty('data/vnexpressrss_news_link.txt'):
            RssExtractor().load()
        self.log.info('Getting news links')
        with open('data/vnexpressrss_news_link.txt', 'r') as f:
            self.link = [i[:-1] for i in f.readlines()]
            self.log.info('Successfully getting rss links')

    def debug(self):
        return self.link

    def extract_news(self, link):
        pass

    def extract(self):
        for i in self.link:
            news = self.extract_news(i)



if __name__ == '__main__':
    extractor = NewsExtractor()
    print(extractor.debug())

