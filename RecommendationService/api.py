import json

from models import (
    get_labels_by_user_id,
    get_users_by_label,
)

from nameko.web.handlers import http


class RecommendationApi:
    name = 'recommnedation_api'

    @http('GET', '/<int:user_id>')
    def get_recommendations_by_user(self, request, user_id):
        """Get recommendations by user_id"""
        try:
            response_object = get_labels_by_user_id(user_id)
            return 201, json.dumps(response_object)
        except Exception as ex:
            error_response(500, ex)

    @http('GET', '/<string:label>')
    def get_users_recomendations_by_label(label):
        """Get users recommendations by label"""
        try:
            response_object = get_users_by_label(label)
            return 200, json.dumps(response_object)
        except Exception as ex:
            error_response(500, ex)


def error_response(code, ex):
    response_object = {
        'status': 'fail',
        'message': str(ex),
    }
    return code, json.dumps(response_object)