-Tener python instalado
-Tener Flask instalado (pip3 install flask pika)
-Ejecutar rabbitMQ con docker:

docker pull rabbitmq:management  

docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
  

-ejecutar el consumidor 
-ejercutar el producer 

-abrir una nueva terminal y enviar un mensaje a la cola : 

curl -X POST "http://127.0.0.1:5000/enqueue?queue=prueba_queue" -H "Content-Type: application/json" -d '{"key": "value"}'