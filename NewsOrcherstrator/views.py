import app
import datetime
import mongoengine

from schema import News

from flask import Blueprint, jsonify, request
from nameko.standalone.rpc import ClusterRpcProxy


news = Blueprint('news', __name__)
CONFIG_RPC = app.config['QUEUE_HOST']


@news.route('/<string:news_type>/news/<string:news_id>', methods=['GET'])
def get_single_news(news_type, news_id):
    """Get single user details"""
    response_object = {
        'status': 'fail',
        'message': 'User does not exist'
    }
    try:
        with ClusterRpcProxy(CONFIG_RPC) as rpc:
            news = rpc.query_famous.get_news(news_id)
            response_object['message'] = News().dumps(news).data
            return jsonify(response_object), 200
    except mongoengine.DoesNotExist:
        return jsonify(response_object), 404


@news.route(
    '/<string:news_type>/news/<int:num_page>/<int:limit>',
    methods=['GET'])
def get_all_news(news_type, num_page, limit):
    """Get all users"""
    with ClusterRpcProxy(CONFIG_RPC) as rpc:
        news = rpc.query_famous.get_all_news(num_page, limit)
        news_list = [
            News().dumps(n).data
            for n in news
        ]
        response_object = {
            'status': 'success',
            'data': news_list,
        }
    return jsonify(response_object), 200


@news.route('/<string:news_type>/news', methods=['POST'])
def add_news(news_type):
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    with ClusterRpcProxy(CONFIG_RPC) as rpc:
        news = rpc.command_famous.create_news(post_data)
        response_object = {
            'status': 'success',
            'news': News().dumps(news).data,
        }
        return jsonify(response_object), 201


@news.route(
    '/<string:news_type>/news/<string:news_id>/publish/',
    methods=['GET'])
def publish_news(news_type, news_id):
    try:
        with ClusterRpcProxy(CONFIG_RPC) as rpc:
            data = rpc.query_famous.get_news(news_id)
            data = News().dumps(data).data
            data['published_at'] = datetime.datetime.utcnow
            news = rpc.command_famous.create_news(data)
            response_object = {
                'status': 'success',
                'news': News().dumps(news).data,
            }
        return jsonify(response_object), 200
    except mongoengine.DoesNotExist:
        return jsonify(response_object), 404


@news.route('/<string:news_type>/news', methods=['PUT'])
def update_news(news_type):
    try:
        post_data = request.get_json()
        if not post_data:
            response_object = {
                'status': 'fail',
                'message': 'Invalid payload.'
            }
            return jsonify(response_object), 400
        with ClusterRpcProxy(CONFIG_RPC) as rpc:
            news = rpc.command_famous.create_news(post_data)
            response_object = {
                'status': 'success',
                'news': News().dumps(news).data,
            }
            return jsonify(response_object), 200
    except mongoengine.DoesNotExist:
        return jsonify(response_object), 404
