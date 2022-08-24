from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass
class NewsEntity:
    cluster_id: int
    date_created: str
    title: str
    description: str
    partner_title: str
    partner_seo_title: str
    category: str
    language: str
    is_main: bool
    url: str
    # created_at: datetime

    def is_later_then(self, minutes):
        pass

    def is_valid_url(self) -> bool:
        return bool(urlparse(self.url).scheme)

# asdict(NewsEntity)
