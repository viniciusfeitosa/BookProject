import os

from datetime import datetime

from py2neo import (
    Graph,
    Node,
    Relationship,
)

USERS_NODE = 'Users'
LABELS_NODE = 'Labels'
REL_TYPE = 'Recommendation'

graph = Graph(os.getenv('DATABASE_URL'))


def get_user_node(user_id):
    return graph.find_one(
        USERS_NODE,
        property_key='id',
        property_value=user_id,
    )


def get_label_node(label):
    return graph.find_one(
        LABELS_NODE,
        property_key='label',
        property_value=label,
    )


def get_labels_by_user_id(user_id):
    user_node = get_user_node(user_id)
    return graph.match(
        start_node=user_node,
        rel_type=REL_TYPE,
    )


def get_users_by_label(label):
    label_node = get_label_node(label)
    return graph.match(
        start_node=label_node,
        rel_type=REL_TYPE,
    )


def create_user_node(user_id):
    # get user info from UsersService
    user_node = Node(USERS_NODE, id=user_id)
    graph.create(user_node)


def create_label_node(label):
    # get user info from UsersService
    label_node = Node(LABELS_NODE, id=label)
    graph.create(label_node)


def create_recommendation(user_id, label):
    user_node = get_user_node(user_id)
    label_node = get_label_node(label)
    Relationship(
        user_node,
        REL_TYPE,
        label_node,
        since=datetime.utcnow(),
    )
