from py2neo import (
    Graph,
)

graph = Graph('http://recommendation_db:7474/db/data')


def add_node(user_data, news_data):
    for labels in news_data.labels:
        pass
