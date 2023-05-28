import pika
import pickle

from capstone import database

RABBITMQ_SERVER_IP = '203.255.57.129'
RABBITMQ_SERVER_PORT = '5672'

credentials = pika.PlainCredentials('rabbitmq', '1q2w3e4r')
connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_SERVER_IP, RABBITMQ_SERVER_PORT, 'vhost', credentials))

channel = connection.channel()

channel.exchange_declare(exchange='input', exchange_type='direct')
channel.exchange_declare(exchange='output', exchange_type='direct')

    

# when user create -> user's exchange also create
def make_exchange(exchange_name):
    channel.exchange_declare(exchange=exchange_name, exchange_type='direct')
    return True


# drone_stop
def rm_queue_message(queue_name):
    while True:
        method_frame,_,body = channel.basic_get(queue=queue_name, auto_ack=True)
        if method_frame:
            print('Delete message : ', body)
        else:
            break



# for mongodb consumer -> save GPS info
class Logging_Consumer():
    
    def __init__(self):
        self.credentials = pika.PlainCredentials('rabbitmq', '1q2w3e4r')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_SERVER_IP, RABBITMQ_SERVER_PORT, 'vhost', self.credentials))
        self.channel = self.connection.channel()

        self.my_name = '[Logging_Consumer]'
        
        self.exchange_name = 'monitoring'
        self.queue_name = 'log_queue'

        # Queue 선언
        queue = self.channel.queue_declare(self.queue_name)
        # Exchange 선언
        self.channel.exchange_declare(self.exchange_name)
        # Queue-Exchange Binding
        self.channel.queue_bind(exchange=self.exchange_name, queue=self.queue_name, routing_key=f'to{self.queue_name}')

    
    def callback(self, ch, method, properties, body):
        log = pickle.loads(body, encoding='bytes')
        database.insert_log(log)
        print(f'{self.my_name} Log_info : ', log)
        
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def consume(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(on_message_callback=self.callback, queue=self.queue_name)
        print(f'{self.my_name} Start Consuming')
        self.channel.start_consuming()



# for drone_control
class Task_Publisher():
    
    def __init__(self):
        self.credentials = pika.PlainCredentials('rabbitmq', '1q2w3e4r')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_SERVER_IP, RABBITMQ_SERVER_PORT, 'vhost', self.credentials))
        self.channel = self.connection.channel()
        
        self.exchange_name = 'input'

    
    def publish_list(self, messages, drone_name):
        
        for message in messages:
            self.channel.basic_publish(
                exchange=self.exchange_name,
                routing_key=f'to{drone_name}',
                body=pickle.dumps(message)
            )
        return True