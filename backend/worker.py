import os
import json
import time
import pika

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
QUEUE_NAME = "order_processing"


def process_order(order_data):
    print(f"[✓] Sipariş işleniyor: {order_data}")
    print("    → Onay maili gönderiliyor...")
    time.sleep(2)  
    print("    → Stok güncelleniyor...")
    time.sleep(1)
    print(f"[✓] Sipariş {order_data['order_id']} işlendi!\n")


def callback(ch, method, properties, body):
    order_data = json.loads(body)
    process_order(order_data)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

    print("[*] Worker başladı. Sipariş bekleniyor... (çıkmak için CTRL+C)")
    channel.start_consuming()


if __name__ == "__main__":
    main()