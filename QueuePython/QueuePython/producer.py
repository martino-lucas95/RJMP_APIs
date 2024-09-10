from flask import Flask, request, jsonify
import pika
import json

app = Flask(__name__)

def get_rabbitmq_channel():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672))
    channel = connection.channel()
    # Asegura que la cola existe
    channel.queue_declare(queue='task_queue', durable=True)
    channel.queue_declare(queue='prueba_queue', durable=True)
    return channel, connection

@app.route('/enqueue', methods=['POST'])
def enqueue_message():
    data = request.json
    message = json.dumps(data)
    queue = request.args.get('queue', 'task_queue')  # Obtiene la cola a usar 
    
    channel, connection = get_rabbitmq_channel()

    # Envia mensaje a la cola
    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # Hace que el mensaje sea persistente
        ))

    connection.close()

    return jsonify({'status': 'Message sent to queue', 'message': message, 'queue': queue}), 200

if __name__ == '__main__':
    app.run(debug=True)
