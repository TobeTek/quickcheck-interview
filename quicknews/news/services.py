from datetime import datetime, timedelta
from typing import cast, Any
import logging

import requests
from requests.adapters import HTTPAdapter, Retry

from news.models import NewsItem, NewsItemTypes

from django.conf import settings
from django.db.utils import IntegrityError

logging.basicConfig()
logger = logging.getLogger(__name__)


class HackerNewsData:
    API_URL = "https://hacker-news.firebaseio.com/v0/"

    session = requests.Session()
    retries = Retry(total=10, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount(API_URL, HTTPAdapter(max_retries=retries))

    @classmethod
    def get_topstories(cls, max_items: int = 100):
        print("Running Get Top Stories")
        api_url = cls.API_URL + "topstories.json"
        r = cls.session.get(api_url)

        topstories_ids = [i for i in r.json() if type(i) == int]
        topstories_ids = filter_persisted_news_items(topstories_ids)["new"]

        items: list[NewsItem] = []
        for item_id in topstories_ids[:max_items]:
            items.append(cls.get_item_by_id(item_id, perform_save=False))

        return NewsItem.objects.bulk_create(items, ignore_conflicts=True)

    @classmethod
    def get_newstories(cls, max_items: int = 100):
        print("Running Get Top Stories")
        api_url = cls.API_URL + "newstories.json"
        r = cls.session.get(api_url)

        newstories_ids = [i for i in r.json() if type(i) == int]
        newstories_ids = filter_persisted_news_items(newstories_ids)["new"]

        items: list[NewsItem] = []
        for item_id in newstories_ids[:max_items]:
            items.append(cls.get_item_by_id(item_id, perform_save=False))

        return NewsItem.objects.bulk_create(items, ignore_conflicts=True)

    @classmethod
    def get_item_by_id(cls, item_id, perform_save=True):
        item = NewsItem.objects.filter(hn_id=item_id).first()

        if not item:
            api_url = cls.API_URL + f"item/{item_id}.json"
            r = cls.session.get(api_url)
            item_data = r.json()

            item = NewsItem._to_news_item(item_data)

            if parent_id := item_data.get("parent"):
                parent_item: NewsItem = NewsItem.objects.filter(
                    hn_id=parent_id
                ).first()  # type:ignore

                if not parent_item:
                    parent_item = cls.get_item_by_id(parent_id).save()
                item.parent = parent_item

                if item.is_polloption:
                    item.parent_poll = item.parent

            if perform_save:
                try:
                    item.save()
                except IntegrityError as e:
                    if "UNIQUE constraint" in str(e):
                        pass
                    else:
                        raise

            if kids_ids := item_data.get("kids"):
                kids_ids = [i for i in kids_ids if type(i) == int]
                kids_ids = filter_persisted_news_items(kids_ids)["new"]
                for kid_id in kids_ids:
                    cls._schedule_retrieve_item_job(kid_id)

        return item

    @classmethod
    def _schedule_retrieve_item_job(cls, item_id):
        logger.debug(f"SCHEDULE_ID: {item_id}")
        run_time = datetime.now() + timedelta(seconds=30)
        settings.SCHEDULER.add_job(
            cls.get_item_by_id,
            next_run_time=run_time,
            args=(item_id,),
            misfire_grace_time=None,
            id=str(item_id),
            replace_existing=False,
        )


def filter_persisted_news_items(item_ids: list[int]) -> dict[str, list[int]]:
    saved_news_items = NewsItem.objects.filter(hn_id__in=item_ids).values("hn_id")
    saved_items: list[int] = [record["hn_id"] for record in saved_news_items]
    new_items: list[int] = [i for i in item_ids if i not in saved_items]

    return {"persisted": saved_items, "new": new_items}
