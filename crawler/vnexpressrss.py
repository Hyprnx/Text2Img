import requests
from bs4 import BeautifulSoup
from base import BaseClass
from common.check_file_empty import is_file_empty
from common.database_connect import connect_to_database
from common.schema.validator import NewsValidator
import time
import random

db = connect_to_database()
db = db['news']


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
        if is_file_empty('crawler/data/vnexpressrss_rss_link.txt'):
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
        with open('crawler/data/vnexpressrss_news_link.txt', 'w+') as f:
            for link in news_links:
                f.writelines(link + '\n')
            self.log.info("Successfully saved.")

class NewsExtractor(BaseClass):
    def __init__(self):
        super().__init__()
        self.validator = NewsValidator()
        if is_file_empty('crawler/data/vnexpressrss_news_link.txt'):
            RssExtractor().load()
        self.log.info('Getting news links')
        with open('crawler/data/vnexpressrss_news_link.txt', 'r') as f:
            self.link = [i[:-1] for i in f.readlines()]
            self.log.info('Successfully getting rss links')

    def debug(self):
        return self.link

    def extract_news(self, link):
        keys = ["source", "source_url", "title", "sapo", "body", "id", "publish", "keyswords", "cates"]
        news_info = dict((el, "") for el in keys)
        res = requests.get(link).text
        soup = BeautifulSoup(res, 'lxml')
        news_container = soup.find('div', attrs={'class': "sidebar-1"})
        news_info["source"] = "vnexpress"
        news_info["source_url"] = link
        news_info["title"] = news_container.find('h1', attrs={"class": 'title-detail'}).text
        news_info["sapo"] = news_container.find('p', attrs={"class": 'description'}).text
        news_info["body"] = '\n '.join(i.text for i in news_container.findAll('p', attrs={"class": 'Normal'}))
        news_info['id'] = hash(link)
        tags_container = news_container.find('ul', attrs={"data-campaign": 'Header', "class": 'breadcrumb'})
        tags_container = tags_container.findAll('li')
        news_info['tags'] = [i.text for i in tags_container]
        news_info['keywords'] = []
        news_info['cates'] = []
        return news_info

    def extract(self):
        for i, link in enumerate(self.link):
            try:
                self.log.info(f"extracting: {link}")
                news = self.extract_news(link)
                if not self.validator.validate(news):
                    self.log.info(f"{link} failed to validate")
                    continue
                self.log.info(f"Finished extracting {link}, pushing to database")
                db.insert_one(news)
                self.log.info("Pushed to database")
            except BaseException as e:
                self.log.error(f"Error: {e}")
                continue
            finally:
                if i % 20 == 0:
                    time.sleep(random.random())



if __name__ == '__main__':
    # url = 'https://vnexpress.net/ran-doc-chui-vao-ong-nuoc-de-ghep-doi-4380130.html'
    extractor = NewsExtractor()
    from pprint import pprint
    pprint(extractor.extract())

