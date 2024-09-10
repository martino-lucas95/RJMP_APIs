import pika
import json
import time

def process_message(message):
    print(f"Processing message: {message}")
    time.sleep(1)
    print(f"Message processed: {message}")

def callback(ch, method, properties, body):
    message = json.loads(body)
    print(f"Received message: {message}")
    process_message(message)
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Conexión a Rabbit
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672))
channel = connection.channel()

# Asegura que la cola existe
channel.queue_declare(queue='task_queue', durable=True)
channel.queue_declare(queue='prueba_queue', durable=True)

# El consumidor recibirá solo un mensaje a la vez
channel.basic_qos(prefetch_count=1)

# Configuracion consumidor
channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.basic_consume(queue='prueba_queue', on_message_callback=callback)

print("Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
