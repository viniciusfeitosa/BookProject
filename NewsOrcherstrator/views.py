import os
import datetime

from schema import News

from flask import Blueprint, jsonify, request
from nameko.standalone.rpc import ClusterRpcProxy


news = Blueprint('news', __name__)
CONFIG_RPC = {'AMQP_URI': os.environ.get('QUEUE_HOST')}


@news.route('/news/<string:news_type>/<int:news_id>', methods=['GET'])
def get_single_news(news_type, news_id):
    """Get single user details"""
    response_object = {
        'status': 'fail',
        'message': 'User does not exist'
    }
    with ClusterRpcProxy(CONFIG_RPC) as rpc:
        import ipdb
        ipdb.set_trace()
        news = rpc.query_famous.get_news(news_id)
        response_object['message'] = news
        return jsonify(response_object), 200


@news.route(
    '/news/<string:news_type>/<int:num_page>/<int:limit>',
    methods=['GET'])
def get_all_news(news_type, num_page, limit):
    """Get all users"""
    with ClusterRpcProxy(CONFIG_RPC) as rpc:
        import ipdb
        ipdb.set_trace()
        news = rpc.query_famous.get_all_news(num_page, limit)
        response_object = {
            'status': 'success',
            'data': news,
        }
    return jsonify(response_object), 200


@news.route('/news/<string:news_type>', methods=['POST'])
def add_news(news_type):
    print(CONFIG_RPC)
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    with ClusterRpcProxy(CONFIG_RPC) as rpc:
        import ipdb
        ipdb.set_trace()
        news = rpc.command_famous.add_news(post_data)
        response_object = {
            'status': 'success',
            'news': news,
        }
        return jsonify(response_object), 201


@news.route(
    '/news/<string:news_type>/<int:news_id>/publish/',
    methods=['GET'])
def publish_news(news_type, news_id):
    with ClusterRpcProxy(CONFIG_RPC) as rpc:
        import ipdb
        ipdb.set_trace()
        data = rpc.query_famous.get_news(news_id)
        data = News().dumps(data).data
        data['published_at'] = datetime.datetime.utcnow
        news = rpc.command_famous.add_news(data)
        response_object = {
            'status': 'success',
            'news': news,
        }
        return jsonify(response_object), 200


@news.route('/news/<string:news_type>', methods=['PUT'])
def update_news(news_type):
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    with ClusterRpcProxy(CONFIG_RPC) as rpc:
        import ipdb
        ipdb.set_trace()
        news = rpc.command_famous.add_news(post_data)
        response_object = {
            'status': 'success',
            'news': news,
        }
        return jsonify(response_object), 200
