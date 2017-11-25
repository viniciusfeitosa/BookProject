import os


from models import (
    get_labels_by_user_id,
    get_users_by_label,
)

from flask import Blueprint, jsonify


recommendation = Blueprint('recommendation', __name__)
CONFIG_RPC = {'AMQP_URI': os.environ.get('QUEUE_HOST')}
RECOMMENDATION_QUEUE = 'recommendation'


@recommendation.route('/<string:user_id>', methods=['GET'])
def get_recommendations_by_user(user_id):
    """Get recommendations by user_id"""
    try:
        response_object = get_labels_by_user_id(user_id)
        return jsonify(response_object), 200
    except Exception as ex:
        erro_response(ex, 500)


@recommendation.route('/<string:label>', methods=['GET'])
def get_users_recomendations_by_label(label):
    """Get users recommendations by label"""
    try:
        response_object = get_users_by_label(label)
        return jsonify(response_object), 200
    except Exception as ex:
        erro_response(ex, 500)


def erro_response(ex, code):
    response_object = {
        'status': 'fail',
        'message': str(ex),
    }
    return jsonify(response_object), code
