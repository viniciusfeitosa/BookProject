import os
import pika


def reader(channel, method, properties, body):
    print('Received {}'.format(body))


class Subscriber:
    def __init__(self):
        self._connection = None
        self._channel = None

    def __get_connection(self):
        if not self._connection:
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=os.environ.get('QUEUE_HOST')))

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
        if self._channel:
            self._channel.start_consuming()

    def stop(self):
        if self._channel:
            self._channel.stop_consuming()
        self.__close_channel()
        self.__close_connection()

    def read_message(self, callback, queue, no_ack=True):
        self._channel.queue_declare(queue=queue)
        self._channel.basic_consume(
            callback,
            queue=queue,
            no_ack=no_ack,
        )
