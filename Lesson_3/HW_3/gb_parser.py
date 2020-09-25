import bs4
import requests
from pymongo import MongoClient


class GbBlogParser(object):
    pass





class GbBlogParser:
    __headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0",
    }

    def __init__(self, domain):
        self.domain = domain
        self.start_url = f'{self.domain}/posts'
        self.urls_pag = set()
        self.done_urls = set()
        self.post_urls = set()
        self.mo_client = MongoClient('mongodb://localhost:27017')



    def get_soup(self, url):
        # todo сделать обработку статус кодов и ошибок
        response = requests.get(url, headers=self.__headers)
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        self.done_urls.add(url)
        return soup

    def get_pagination(self, soup):
        ul = soup.find('ul', attrs={'class': "gb__pagination"})
        li = ul.find_all('li')
        links = {f'{self.domain}{itm.find("a").attrs.get("href")}' for itm in li if itm.find('a').attrs.get('href')}
        return links

    # todo найти список постов и вернуть список url на посты
    def get_post_urls(self, soup):
        wrapper = soup.find('div', attrs={'class': "post-items-wrapper"})
        posts = wrapper.find_all('div', attrs={'class': "post-item"})
        links = {f'{self.domain}{itm.find("a").attrs.get("href")}' for itm in posts if itm.find('a').attrs.get('href')}
        return links

    def parse(self):
        url = self.start_url
        while url:
            soup = self.get_soup(url)
            self.urls_pag.update(self.get_pagination(soup))
            self.urls_pag.difference_update(self.done_urls)
            url = self.urls_pag.pop() if self.urls_pag else None
            self.post_urls.update(self.get_post_urls(soup))
        for page_url in self.post_urls:
            print(f'page parser is starting {page_url}')
            self.page_parse(page_url)



    def get_page_soup(self, page_url):
        self.page_url = page_url
        response = requests.get(page_url, headers=self.__headers)
        page_soup = bs4.BeautifulSoup(response.text, 'lxml')
        print('page soup is done')
        return page_soup

    def page_parse(self, page_url):
        page_soup = self.get_page_soup(page_url)
        title = page_soup.find_all('h1', attrs={'class': 'blogpost-title'})
        self.title = title[-1].getText()
        try:
            self.image_url = page_soup.find('div', attrs={'class': 'blogpost-content'}).find('img').get('src')
        except:
            self.image_url = 'None'
        writer_name = page_soup.find_all('div', attrs={'itemprop': 'author'})
        self.writer_name = writer_name[-1].getText()
        pub_date = page_soup.find_all('time', attrs={'itemprop': 'datePublished'})
        self.pub_date = pub_date[-1].getText()
        self.writer_url = page_soup.find('a', attrs={'style': 'text-decoration:none;'}).get('href')
        self.tag_names = [itm.getText() for itm in page_soup.find_all('a', attrs={'class': 'small'})]
        self.tag_links = [f'https://geekbrains.ru{itm.get("href")}' for itm in page_soup.find_all('a', attrs={'class': 'small'})]
        self.save_to_mongo({
                            'title': self.title,
                            'url': self.page_url,
                            'image_url': self.image_url,
                            'writer_name': self.writer_name,
                            'writer_url': f'https://geekbrains.ru{self.writer_url}',
                            'pub_date': self.pub_date,
                            'tag_names': self.tag_names,
                            'tag_links': self.tag_links
                            })

    # todo сохранить в БД
    def save_to_mongo(self, data: dict):
        db = self.mo_client['my_db']
        collection = db['gb_posts']
        collection.insert_one(data)
        print('post was saved to MongoDB')


if __name__ == '__main__':
    parser = GbBlogParser('https://geekbrains.ru')
    parser.parse()


