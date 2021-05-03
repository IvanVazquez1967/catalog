import pika, json

params = pika.URLParameters('amqps://uheyjeyc:ZohEvjdhz19YAUKQXPs3Mp-Lb5QXEvZ4@gull.rmq.cloudamqp.com/uheyjeyc')

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)


