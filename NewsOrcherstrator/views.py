import os
import datetime
import json

from flask import Blueprint, jsonify, request
from nameko.standalone.rpc import ClusterRpcProxy


news = Blueprint('news', __name__)
CONFIG_RPC = {'AMQP_URI': os.environ.get('QUEUE_HOST')}


@news.route('/news/<string:news_type>/<int:news_id>', methods=['GET'])
def get_single_news(news_type, news_id):
    """Get single user details"""
    try:
        with ClusterRpcProxy(CONFIG_RPC) as rpc:
            news = rpc.query_famous.get_news(news_id)
            response_object = {
                'status': 'success',
                'message': json.loads(news)
            }
            return jsonify(response_object), 200
    except Exception as e:
        erro_response(e, 500)


@news.route(
    '/news/<string:news_type>/<int:num_page>/<int:limit>',
    methods=['GET'])
def get_all_news(news_type, num_page, limit):
    """Get all users"""
    try:
        with ClusterRpcProxy(CONFIG_RPC) as rpc:
            news = rpc.query_famous.get_all_news(num_page, limit)
            response_object = {
                'status': 'success',
                'data': json.loads(news),
            }
            return jsonify(response_object), 200
    except Exception as e:
        return erro_response(e, 500)


@news.route('/news/<string:news_type>', methods=['POST'])
def add_news(news_type):
    post_data = request.get_json()
    if not post_data:
        return erro_response('Invalid payload', 400)
    try:
        with ClusterRpcProxy(CONFIG_RPC) as rpc:
            news = rpc.command_famous.add_news(post_data)
            response_object = {
                'status': 'success',
                'news': news,
            }
            return jsonify(response_object), 201
    except Exception as e:
        return erro_response(e, 500)


@news.route('/news/<string:news_type>', methods=['PUT'])
def update_news(news_type):
    post_data = request.get_json()
    if not post_data:
        return erro_response('Invalid Payload', 400)
    try:
        with ClusterRpcProxy(CONFIG_RPC) as rpc:
            news = rpc.command_famous.add_news(post_data)
            response_object = {
                'status': 'success',
                'news': news,
            }
            return jsonify(response_object), 200
    except Exception as e:
        return erro_response(e, 500)


def erro_response(e, code):
    response_object = {
        'status': 'fail',
        'message': str(e),
    }
    return jsonify(response_object), code
