import requests

from nameko.rpc import rpc

from models import (
    create_user_node,
    create_label_node,
    create_recommendation,
)


class Recommendation:
    name = 'recommendation'

    @rpc
    def send(self, data):
        try:
            user = requests.get(
                "http://172.17.0.1/user/{}".format(
                    data['user_id'],
                )
            )
            user = user.json()
            create_user_node(user)
            for label in data['news']['tags']:
                create_label_node(label)
                create_recommendation(
                    user['id'],
                    label,
                )
        except Exception as e:
            print(e)
