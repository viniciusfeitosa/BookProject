from user_service.client import GetUserData

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


class UserClient:
    def __init__(self):
        self.transport = TSocket.TSocket('127.0.0.1', 9090)

        # Buffering is critical. Raw sockets are very slow
        self.transport = TTransport.TBufferedTransport(self.transport)

        # Wrap in a protocol
        protocol = TBinaryProtocol.TBinaryProtocol(self.transport)

        # Create a client to use the protocol encoder
        self.client = GetUserData(protocol)

        # Connect!
        self.transport.open()

    def __exit__(self):
        self.transport.close()

    def get_user(self, id):
        return self.client.get_user(id)
