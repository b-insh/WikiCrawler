from bs4 import BeautifulSoup
import requests

class WikiCrawler(object):
    """
    Wikipedia crawler that an article and follows the first link on the main body of the article on each subsequent page until reaching the Philosophy page
    """

    def __init__(self):
        self.philosophy = '/wiki/Philosophy'

        self.checkable_urls = self._get_urls()

        self.seen_urls = {}
        self.path = {}

    def _get_urls(self):
        payload = {
            "action": "query",
            "format": "json",
            "list": "random",
            "rnnamespace": "0",
            "rnlimit": "5"
        }

        r = requests.get('http://en.wikipedia.org/w/api.php?', params=payload)
        pages = r.json()['query']['random']
        return (['/wiki/' + page['title'].replace(" ", "_") for page in pages])


crawler = WikiCrawler()
# crawler._get_urls()
