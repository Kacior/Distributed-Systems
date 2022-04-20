import pika
import uuid
from pika.exchange_type import ExchangeType
import threading


class SquadClient(object):
    def __init__(self, name):
        self.name = name
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )

        self.channel = self.connection.channel()
        self.channel.exchange_declare('x', exchange_type=ExchangeType.direct)

        result = self.channel.queue_declare(
            queue=f'ack_{self.name}', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def generate_orders(self):
        while True:
            message = input()

            route_to = ''

            if message == 'oxygen':
                route_to = 'oxygen'
            elif message == 'backpack':
                route_to = 'backpack'
            elif message == 'shoes':
                route_to = 'shoes'
            elif message == 'exit':
                self.connection.close()

            if route_to != '':
                order = f"{self.name}.{message}"
                print(order)
                self.response = None
                self.corr_id = str(uuid.uuid4())
                self.channel.basic_publish(
                    exchange='x',
                    routing_key=route_to,
                    body=order,
                    properties=pika.BasicProperties(
                        delivery_mode=2,
                        reply_to=self.callback_queue,
                        correlation_id=self.corr_id
                    )
                )
                while self.response is None:
                    self.connection.process_data_events()
                print(self.response)
            else:
                print(
                    "This product is not avaiable. Only oxygen, shoes and backpacks in stock")


if __name__ == "__main__":
    print("Enter squad name: ")
    name = input()
    squad = SquadClient(name)
    squad.generate_orders()
