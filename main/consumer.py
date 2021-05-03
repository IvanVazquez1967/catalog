import json
import pika

from main import Product, db

params = pika.URLParameters('your amqps instance')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print('Received in main')
    data = json.loads(body)
    print(data)

    if properties.content_type == 'product_created':
        product = Product(
            id=data['id'],
            sku=data['sku'],
            name=data['name'],
            price=data['price'],
            brand=data['brand'],
            image=data['image'],
            views=data['views']
        )
        db.session.add(product)
        db.session.commit()
        print('Product Created')

    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.sku = data['sku']
        product.name = data['name']
        product.price = data['price']
        product.brand = data['brand']
        product.image = data['image']
        product.views = data['views']
        db.session.commit()
        print('Product Updated')

    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print('Product Deleted')


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
