import os
import json

from flask import Blueprint, jsonify, request
from nameko.standalone.rpc import ClusterRpcProxy


news = Blueprint('news', __name__)
CONFIG_RPC = {'AMQP_URI': os.environ.get('QUEUE_HOST')}


@news.route('/<string:news_type>/news/<int:news_id>', methods=['GET'])
def get_single_news(news_type, news_id):
    """Get single user details"""
    try:
        response_object = rpc_get_news(news_type, news_id)
        return jsonify(response_object), 200
    except Exception as e:
        erro_response(e, 500)


@news.route(
    '/<string:news_type>/news/<int:num_page>/<int:limit>',
    methods=['GET'])
def get_all_news(news_type, num_page, limit):
    """Get all users"""
    try:
        response_object = rpc_get_all_news(
            news_type,
            num_page,
            limit
        )
        return jsonify(response_object), 200
    except Exception as e:
        return erro_response(e, 500)


@news.route('/<string:news_type>/news', methods=['POST'])
def add_news(news_type):
    post_data = request.get_json()
    if not post_data:
        return erro_response('Invalid payload', 400)
    try:
        response_object = rpc_command(news_type, post_data)
        return jsonify(response_object), 201
    except Exception as e:
        return erro_response(e, 500)


@news.route('/<string:news_type>/news', methods=['PUT'])
def update_news(news_type):
    post_data = request.get_json()
    if not post_data:
        return erro_response('Invalid Payload', 400)
    try:
        response_object = rpc_command(news_type, post_data)
        return jsonify(response_object), 200
    except Exception as e:
        return erro_response(e, 500)


def erro_response(e, code):
    response_object = {
        'status': 'fail',
        'message': str(e),
    }
    return jsonify(response_object), code


def rpc_get_news(news_type, news_id):
    with ClusterRpcProxy(CONFIG_RPC) as rpc:
        if news_type == 'famous':
            news = rpc.query_famous.get_news(news_id)
        elif news_type == 'sports':
            news = rpc.query_sports.get_news(news_id)
        elif news_type == 'politics':
            news = rpc.query_politics.get_news(news_id)
        else:
            return erro_response('Invalid News type', 400)
        return {
            'status': 'success',
            'message': json.loads(news)
        }


def rpc_get_all_news(news_type, num_page, limit):
    with ClusterRpcProxy(CONFIG_RPC) as rpc:
        if news_type == 'famous':
            news = rpc.query_famous.get_all_news(num_page, limit)
        elif news_type == 'sports':
            news = rpc.query_sports.get_all_news(num_page, limit)
        elif news_type == 'politics':
            news = rpc.query_politics.get_all_news(num_page, limit)
        else:
            return erro_response('Invalid News type', 400)
        return {
            'status': 'success',
            'message': json.loads(news)
        }


def rpc_command(news_type, data):
    with ClusterRpcProxy(CONFIG_RPC) as rpc:
        if news_type == 'famous':
            news = rpc.command_famous.add_news(data)
        elif news_type == 'sports':
            news = rpc.command_sports.add_news(data)
        elif news_type == 'politics':
            news = rpc.command_politics.add_news(data)
        else:
            return erro_response('Invalid News type', 400)
        return {
            'status': 'success',
            'news': news,
        }
