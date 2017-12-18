import os
import grpc

import user_data_pb2
import user_data_pb2_grpc


class UserClient:
    def __init__(self, user_id):
        self.user_id = int(user_id)
        self.channel = grpc.insecure_channel(os.getenv('USER_SERVICE_HOST'))
        self.stub = user_data_pb2_grpc.GetUserDataStub(self.channel)

    def __enter__(self):
        return self.stub.GetUser(
            user_data_pb2.UserDataRequest(id=self.user_id)
        )

    def __exit__(self, type, value, traceback):
        pass
