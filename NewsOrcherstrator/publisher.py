import os
import pika


class Publisher:
    def __init__(self):
        self._connection = None
        self._channel = None

    def __get_connection(self):
        if not self._connection:
            self._connection = pika.BlockingConnection(
                pika.URLParameters(os.environ.get('QUEUE_HOST'))
            )

    def __get_channel(self):
        if not self._channel:
            self._channel = self._connection.channel()

    def __close_connection(self):
        if self._connection:
            self._connection.close()

    def __close_channel(self):
        if self._channel:
            self._channel.close()

    def start(self):
        self.__get_connection()
        self.__get_channel()

    @classmethod
    def get_instance(cls):
        if not cls._connection and not cls._channel:
            cls.start()
        return cls

    def stop(self):
        self.__close_channel()
        self.__close_connection()

    def send_message(self, queue, routing_key, data):
        self._channel.queue_declare(queue=queue)
        self._channel.basic_publish(
            exchange='',
            routing_key=routing_key,
            body=data,
        )
