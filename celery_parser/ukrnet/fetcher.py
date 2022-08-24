from requests import Session
from fake_useragent import UserAgent
from typing import List
from pprint import pprint
from ukrnet.dto import NewsEntity
import validators
from ukrnet.formatter import NewsFormatter
from retrying import retry


class NewsFetcher:
    ALLOWED_CATEGORIES = ["politika", "jekonomika", "proisshestvija", "society", "tehnologii", "science",
                          "avto", "sport", "zdorove", "show_biznes"]

    _api_url_template: str = "https://www.ukr.net/news/dat/{category}/{page}/"

    def __init__(self, session: Session = None):
        # self._fetcher = NewsFetcher()
        # self._formatter = NewsFormatter()
        self.session = session or Session()
        self.session.headers.update({
            "User-Agent": UserAgent().random
        })

    def request_api(self, category: str, page: int = 1) -> object:
        if category not in self.ALLOWED_CATEGORIES:
            raise ValueError("Invalid category value!")

        api_url = self._api_url_template.format(category=category, page=page)
        json_response = self.session.get(api_url, timeout=15).json()
        news_records = json_response["tops"]
        news_data: List[dict] = list()

        for record in news_records:
            for key in ["News", "Dups"]:
                if key in record:
                    record["IsMain"] = True
                    news_data.extend(record.pop(key))

            news_data.append(record)

        for record in news_data:
            record["Category"] = category
        return news_data


class Controller:

    def __init__(self):
        self.fetcher = NewsFetcher()
        self.formatter = NewsFormatter()

    @retry(stop_max_attempt_number=3)
    def get_last_news(self) -> List[NewsEntity]:
        all_categories = self.fetcher.ALLOWED_CATEGORIES
        all_news = list()
        formatted_news = list()
        for category in all_categories:
            temp_list = []
            while True:
                page = 1
                fetch_json = self.fetcher.request_api(category=category, page=page)
                for news in fetch_json:
                    temp_list.append(news)
                for news in temp_list:
                    all_news.append(news)
                break
        for news_data in all_news:
            formatted_data: NewsEntity = self.formatter.reformat_news_item(news_data)
            if validators.url(formatted_data.url):
                formatted_news.append(formatted_data)

        return formatted_news

    def _process_news(self):
        pass


if __name__ == '__main__':
    ukrnet = Controller()
    b = ukrnet.get_last_news()
    pprint(b)
