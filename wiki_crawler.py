from bs4 import BeautifulSoup
from collections import Counter
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

        while len(self.seen_urls.keys()) < 500:
            print ("~" * 40)
            self.crawl(self.checkable_urls.pop())

        percentage = self._get_percentage()
        distribution = self._get_distribution()
        average = self._get_average()

        print ('Percentage of links that get to Philosophy: %.2f' % percentage)
        print ('Average number of steps to Philosophy:', average)
        print ('Distribution of number of links to get to Philosophy:')
        for dist_pair in distribution:
            if dist_pair[0]:
                print (dist_pair[1], "links were ", dist_pair[0], "clicks away from Philosophy")

    def crawl(self, url):
        """
        Checks if the url is one we have seen before, if not, finds its first link and continues tracking how many links away it is
        """

        philosophy = '/wiki/Philosophy'
        links_away = 1

        while not url == philosophy:
            print (url)
            if url in self.seen_urls:
                if not self.seen_urls[url]:
                    self.clear_path(links_away, False)
                else:
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

    def get_next_url(self, url):
        """
        Scrapes through current url's html to find first valid link, returns False if there isn't one.
        """

        page = self.base_url + url
        response = requests.get(page).content
        soup = self.make_soup(response, 'div#mw-content-text > p')
        if soup.find('a') is None:
            soup = self.make_soup(response, 'div#mw-content-text')
            if soup.find('a') is None:
                return False

        return self.clean_url((soup.find('a')['href']))

    def make_soup(self, response, tag):
        """ Creates html soup from current page """

        soup = self.clean_soup(BeautifulSoup(response, 'html.parser'))
        body = self.remove_parens(str(soup.select(tag)))
        return BeautifulSoup(body, 'html.parser')

    def clean_soup(self, soup):
        """ Removes unneccessary tags and links from body of page """

        [tag.extract() for tag in soup.find_all('i')]
        [tag.extract() for tag in soup.find_all('sup')]
        [tag.extract() for tag in soup.find_all('span')]
        [tag.extract() for tag in soup.find_all('small')]
        [tag.extract() for tag in soup.find_all('table')]
        [out_link.extract() for out_link in soup.find_all('a', { 'class': 'extiw' })]
        [out_link.extract() for out_link in soup.find_all('a', { 'class': 'new' })]
        [out_link.extract() for out_link in soup.find_all('a', { 'class': 'external text' })]
        [out_link.extract() for out_link in soup.find_all('a', { 'class': 'image' })]
        [bad_link.extract() for bad_link in soup.find_all('div', { 'class': 'toc' })]
        [bad_link.extract() for bad_link in soup.find_all('div', { 'class': 'thumb' })]

        return soup

    def clean_url(self, url):
        """ Returns the relative url in case the href found is an absolute url """

        return url[url.find("/wiki/"):]

    def remove_parens(self, body):
        """ Removes parentheses and enclosed text from the page if it is not between quotes """

        return regex.sub(r'".*?\(*.*?\)*.*?"(*SKIP)(*FAIL)|\(.*?\)', '', body)

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

    def _get_average(self):
        values = self._get_distribution()
        total_clicks = 0
        for value in values:
            total_clicks += (value[0] * value[1])
        return total_clicks / 500

    def _get_distribution(self):
        """ Gets distribution of paths to Philosophy and their lengths """

        return Counter(self.seen_urls.values()).most_common()

    def _get_percentage(self):
        """ Calcuates percentage of links that get to Philosophy """

        valid_paths = len([url for url in self.seen_urls if self.seen_urls[url]])
        return (valid_paths / len(self.seen_urls)) * 100

    def _get_urls(self):
        """ Gets 500 random urls from the Wikipedia API in one HTTP Request """

        payload = {
            "action": "query",
            "format": "json",
            "list": "random",
            "rnnamespace": "0",
            "rnlimit": "500"
        }

        response = requests.get('http://en.wikipedia.org/w/api.php?', params=payload)
        pages = response.json()['query']['random']
        return ['/wiki/' + page['title'].replace(" ", "_") for page in pages]


crawler = WikiCrawler()
crawler.start()
