from bs4 import BeautifulSoup
import requests
import regex

class WikiCrawler(object):
    """
    Wikipedia crawler that takes an article and follows the first link on the main body of the article until reaching the Philosophy page
    """

    def __init__(self):
        self.base_url = 'http://en.wikipedia.org'

        self.checkable_urls = self._get_urls()

        self.seen_urls = {}
        self.path = {}

    def start(self):
        """ Cycles through each of the randomly generated urls """

        for url in self.checkable_urls:
            self.crawl(url)



    def crawl(self, url):
        """
        Checks if the url is one we have seen before, if not, we find its first link and continue tracking how many links away it is
        """

        philosophy = '/wiki/Philosophy'
        links_away = 1

        while not url == philosophy:
            print (url)
            if url in self.seen_urls:
                links_away += self.seen_urls[url] + 1

                self.clear_path(links_away)
                break

            elif url in self.path or not url:
                self.clear_path(links_away, False)
                break
            else:
                links_away += 1
                self.path[url] = links_away
                url = self.get_next_url(url)

        links_away += 1
        self.clear_path(links_away)
        print (self.seen_urls)

    def get_next_url(self, url):
        page = self.base_url + url
        response = requests.get(page).content
        soup = self.clean_soup(BeautifulSoup(response, 'html.parser'))
        if soup.find('a') is None:
            return self.check_elsewhere(response)
        return self.clean_url((soup.find('a')['href']))

    def check_elsewhere(self, response):
        soup = (BeautifulSoup(response, 'html.parser'))
        [tag.replaceWith("") for tag in soup.find_all('sup')]
        [tag.replaceWith("") for tag in soup.find_all('span')]
        [tag.replaceWith("") for tag in soup.find_all('i')]
        [out_link.replaceWith("") for out_link in soup.find_all('a', { 'class': 'extiw' })]

        body = self.remove_parens(str(soup.select('div#mw-content-text')))
        soup = BeautifulSoup(body, 'html.parser')
        if soup.find('a') is None:
            return False
        return self.clean_url((soup.find('a')['href']))


    def clean_soup(self, soup):
        """ Remove unneccessary tags and links from body of page """
        [tag.replaceWith("") for tag in soup.find_all('sup')]
        [tag.replaceWith("") for tag in soup.find_all('span')]
        [tag.replaceWith("") for tag in soup.find_all('i')]
        [out_link.replaceWith("") for out_link in soup.find_all('a', { 'class': 'extiw' })]

        body = self.remove_parens(str(soup.select('div#mw-content-text > p')))
        return BeautifulSoup(body, 'html.parser')
        # [out_link.replaceWith("") for out_link in soup.find_all('div', { 'class': 'hatnote' })]
        # [out_link.replaceWith("") for out_link in soup.find_all('a', { 'class': 'mw-redirect' })]

    def clean_url(self, url):
        """ Returns the relative url if the href found is an absolute url """
        if url[0:4] == "http":
            url = url[url.find("/wiki/"):]
            print ("chopped")
            print (url)
        return url

    def remove_parens(self, body):
        """ Removes parentheses and enclosed text from the page """
        return regex.sub(r'".*?\(.*?\).*?"(*SKIP)(*FAIL)|\(.*?\)', '', body)

    def clear_path(self, links_away, valid_url = True):
        """
        Takes all links in the current path and memoizes them in a dictionary. The url is the key and distance from philosophy is the value. If the link is invalid, the value is False.
        """
        for url in self.path:
            if url not in self.seen_urls:
                if valid_url:
                    self.seen_urls[url] = links_away - self.path[url]
                else:
                    self.seen_urls[url] = False

        self.path = {}

    def _get_urls(self):
        """ Gets all 500 urls from the Wikipedia API in one HTTP Request """

        payload = {
            "action": "query",
            "format": "json",
            "list": "random",
            "rnnamespace": "0",
            "rnlimit": "10"
        }

        response = requests.get('http://en.wikipedia.org/w/api.php?', params=payload)
        pages = response.json()['query']['random']
        return ['/wiki/' + page['title'].replace(" ", "_") for page in pages]


crawler = WikiCrawler()
crawler.start()
# crawler.get_next_url('/wiki/Physics')
# crawler.crawl('/wiki/Gegenbauer')
