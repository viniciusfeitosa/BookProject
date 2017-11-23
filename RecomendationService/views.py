import os
import json
import itertools

from flask import Blueprint, jsonify, request
from nameko.standalone.rpc import ClusterRpcProxy


recomendation = Blueprint('recomendation', __name__)
CONFIG_RPC = {'AMQP_URI': os.environ.get('QUEUE_HOST')}


@recomendation.route('/<string:news_type>/<int:news_id>', methods=['GET'])
def get_single_news(news_type, news_id):
    """Get single user details"""
    try:
        response_object = rpc_get_news(news_type, news_id)
        return jsonify(response_object), 200
    except Exception as e:
        erro_response(e, 500)


@recomendation.route(
    '/all/<int:num_page>/<int:limit>',
    methods=['GET'])
def get_all_news(num_page, limit):
    try:
        response_famous = rpc_get_all_news(
            'famous',
            num_page,
            limit
        )
        response_politics = rpc_get_all_news(
            'politics',
            num_page,
            limit
        )
        response_sports = rpc_get_all_news(
            'sports',
            num_page,
            limit
        )
        all_news = itertools.chain(
            response_famous.get('recomendation', []),
            response_politics.get('recomendation', []),
            response_sports.get('recomendation', []),
        )
        response_object = {
            'status': 'success',
            'recomendation': list(all_news),
        }
        return jsonify(response_object), 200
    except Exception as e:
        return erro_response(e, 500)


@recomendation.route(
    '/<string:news_type>/<int:num_page>/<int:limit>',
    methods=['GET'])
def get_all_news_per_type(news_type, num_page, limit):
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


@recomendation.route('/<string:news_type>', methods=['POST'])
def add_news(news_type):
    post_data = request.get_json()
    if not post_data:
        return erro_response('Invalid payload', 400)
    try:
        response_object = rpc_command(news_type, post_data)
        return jsonify(response_object), 201
    except Exception as e:
        return erro_response(e, 500)


@recomendation.route('/<string:news_type>', methods=['PUT'])
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
            recomendation = rpc.query_famous.get_news(news_id)
        elif news_type == 'sports':
            recomendation = rpc.query_sports.get_news(news_id)
        elif news_type == 'politics':
            recomendation = rpc.query_politics.get_news(news_id)
        else:
            return erro_response('Invalid recomendation type', 400)
        return {
            'status': 'success',
            'recomendation': json.loads(recomendation)
        }


def rpc_get_all_news(news_type, num_page, limit):
    with ClusterRpcProxy(CONFIG_RPC) as rpc:
        if news_type == 'famous':
            recomendation = rpc.query_famous.get_all_news(num_page, limit)
        elif news_type == 'sports':
            recomendation = rpc.query_sports.get_all_news(num_page, limit)
        elif news_type == 'politics':
            recomendation = rpc.query_politics.get_all_news(num_page, limit)
        else:
            return erro_response('Invalid recomendation type', 400)
        return {
            'status': 'success',
            'recomendation': json.loads(recomendation)
        }


def rpc_command(news_type, data):
    with ClusterRpcProxy(CONFIG_RPC) as rpc:
        if news_type == 'famous':
            recomendation = rpc.command_famous.add_news(data)
        elif news_type == 'sports':
            recomendation = rpc.command_sports.add_news(data)
        elif news_type == 'politics':
            recomendation = rpc.command_politics.add_news(data)
        else:
            return erro_response('Invalid recomendation type', 400)
        return {
            'status': 'success',
            'recomendation': recomendation,
        }
