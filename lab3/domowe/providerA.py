import pika
from pika.exchange_type import ExchangeType


class Provider(object):
    def __init__(self, name):
        self.name = name
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = self.connection.channel()

        self.channel.exchange_declare(
            exchange='x', exchange_type=ExchangeType.direct)
        self.channel.queue_declare('oxygen', durable=True)
        self.channel.queue_declare('shoes', durable=True)

        self.channel.queue_bind(
            exchange='x', queue='oxygen', routing_key='oxygen')

        self.channel.queue_bind(
            exchange='x', queue='shoes', routing_key='shoes')
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='oxygen',
                                   on_message_callback=self.callback)

        self.channel.basic_consume(
            queue='shoes', on_message_callback=self.callback)

    def start_consuming(self):
        print('[*] Waiting for orders.')
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        data = body.decode().split(".")
        buyer = data[0]
        item = data[1]
        print(f"[x] Received {item} request from {buyer}")
        print(f" [x] Shipment for {buyer} Done")

        reply = f"Hello {buyer}, your order for {item} has been completed by {self.name}"

        ch.basic_publish(exchange='', routing_key=properties.reply_to, properties=pika.BasicProperties(
            correlation_id=properties.correlation_id
        ), body=reply)

        ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    print("Enter provider name:")
    name = input()
    provider = Provider(name)
    provider.start_consuming()
