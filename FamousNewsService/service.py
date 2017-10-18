import mongoengine

from models import (
    session,
    CommandNewsModel,
    QueryNewsModel,
)

from nameko.events import EventDispatcher
from nameko.rpc import rpc
from nameko.events import event_handler


class Command:
    name = 'command_famous'
    dispatch = EventDispatcher()

    @rpc
    def add_news(self, data):
        try:
            news_version = 1
            if data.get('news_version'):
                news_version = data.get('news_version') + 1
            news = CommandNewsModel(
                news_version=news_version,
                title=data['title'],
                content=data['content'],
                author=data['author'],
                published_at=data.get('published_at'),
                tags=data['tags'],
            )
            session.add(news)
            session.commit()
            data['id'] = news.id
            data['news_version'] = news.news_version
            self.dispatch('replicate_db_event', data)
            return data
        except Exception as e:
            return e


class Query:
    name = 'query_famous'

    @event_handler('command_famous', 'replicate_db_event')
    def normalize_db(self, data):
        try:
            news = QueryNewsModel.objects.get(
                id=data['news_version']
            )
            news.update(
                news_version=data.get('news_version', news.news_version),
                title=data.get('title', news.title),
                content=data.get('content', news.content),
                author=data.get('author', news.author),
                published_at=data.get('published_at', news.author),
                tags=data.get('tags', news.tags),
            )
            news.reload()
        except mongoengine.DoesNotExist:
            QueryNewsModel(
                id=data['id'],
                news_version=data['news_version'],
                title=data.get('title'),
                content=data.get('content'),
                author=data.get('author'),
                tags=data.get('tags'),
            ).save()
        except Exception as e:
            return e

    @rpc
    def get_news(self, id):
        try:
            news = QueryNewsModel.objects.get(id=id)
            return news.to_json()
        except mongoengine.DoesNotExist as e:
            return e
        except Exception as e:
            return e

    @rpc
    def get_all_news(self, num_page, limit):
        try:
            if not num_page:
                num_page = 1
            offset = (num_page - 1) * limit
            news = QueryNewsModel.objects.skip(offset).limit(limit)
            return news.to_json()
        except Exception as e:
            return e
