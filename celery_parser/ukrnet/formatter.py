from .dto import NewsEntity
import fasttext

lid_model = fasttext.load_model('/queue/ukrnet/lid.176.bin')


class NewsFormatter:
    CATEGORY_MAPPING: dict = {
        "politika": "politics",
        "jekonomika": "economy",
        "proisshestvija": "incidents",
        "tehnologii": "technology",
        "avto": "auto",
        "zdorove": "health",
        "show_biznes": "showbiz"
    }

    ACCEPTED_FIELDS: list = ['Category', 'ClusterId',
                             'DateCreated',
                             'NewsId', 'PartnerId',
                             'PartnerSeoTitle', 'PartnerTitle',
                             'Title', 'Url', 'Description']

    UNNECESSARY_FIELDS: list = ["NewsId", "Id", "HasImage",
                                "HasVideo", "Details", "NewsCount",
                                "Transition", "PartnerId", "SeoTitle",
                                "TopValue", "DateLast", "News", "Dups",
                                "OriginalId", "SetUtmSource"]

    def __init__(self):
        pass
        # self._fetcher = NewsFetcher()
        # self._formatter = NewsFormatter()

    def reformat_news_with_template(self, news_item, template):
        pass

    def reformat_news_item(self, news_data) -> dict:
        # TODO: make function for one record, should produce NewsEntity
        # TODO: add lang detect
        # TODO: add category mapping usage

        formatted_data: dict = {}
        if set(self.ACCEPTED_FIELDS).issubset(news_data.keys()):
            formatted_data.update(news_data)
            # formatted_data["DateCreated"] = datetime.fromtimestamp(formatted_data["DateCreated"])
            formatted_data["Description"] = " ".join(formatted_data["Description"].split("\n"))

            formatted_data["Language"] = lid_model.predict(formatted_data["Title"])[0][0].split("__label__")[1]

            formatted_data["IsMain"] = news_data.get("IsMain", False)
            if formatted_data["Category"] in self.CATEGORY_MAPPING:
                formatted_data.update({"Category": self.CATEGORY_MAPPING[formatted_data["Category"]]})
            for unnecessary_field in self.UNNECESSARY_FIELDS:
                if unnecessary_field in formatted_data:
                    del formatted_data[unnecessary_field]
            formatted_data = NewsEntity(
                cluster_id=news_data['ClusterId'],
                date_created=formatted_data["DateCreated"],
                description=formatted_data["Description"],
                partner_title=formatted_data['PartnerTitle'],
                partner_seo_title=formatted_data['PartnerSeoTitle'],
                category=formatted_data['Category'],
                language=formatted_data["Language"],
                is_main=formatted_data["IsMain"],
                url=news_data['Url'],
                title=news_data['Title']
            )
        return formatted_data
