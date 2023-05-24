from rabbit_service import RabbitService
from config import *
import json
import traceback
from datetime import datetime


def send_error_message(topic_name, info, exp):
    args = [ type(exp).__name__, info + " " +
            str(exp), str(datetime.now())]
    service.send_message(topic_name, ERROR_MESSAGE(*args))
    print(f"    [+] Error was sent to '{topic_name}' topic")


def try_deserialize_request(request, required_keys):
    try:
        req = json.loads(request)
        [req[key] for key in required_keys]
        print(req)
        return req
    except Exception as exp:
        print("    [x] Invalid Request")
        print(f"    {type(exp).__name__}: {exp}")
        return None


def on_message_received(channel, method, properties, request):
    print(request)
    print("[+] Received new message")
    req = try_deserialize_request(request, ['dataset'])
    if req is None:
        return

    model_label = req['modelLabel']
    print(f"    [!] Request type: {model_label}")
    if model_label != 'SPLIT':
        print(f"    [x] Invalid request type '{model_label}'")
        return
    try:
        service.send_message(MainTopic.MAIN, split_data(req))
    except Exception as exp:
        print(f"    [x] {type(exp).__name__}: {exp}")
        traceback.print_tb(exp.__traceback__)
        tb_error = ''.join(traceback.format_tb(exp.__traceback__))
        send_error_message(
            MainTopic.ERROR, f"Status: '{model_label}'", tb_error)
    channel.basic_ack(method.delivery_tag)


if __name__ == '__main__':
    service = RabbitService(RabbitConfig.HOST, RabbitConfig.PORT, RabbitConfig.USER, RabbitConfig.PASSWORD)
    service.add_exchange(MainTopic.MAIN, 'topic')
    service.add_exchange(MainTopic.ERROR, 'topic')
    service.add_exchange(ServiceConfig.TOPIC_NAME, 'topic')
    service.add_topic(MainTopic.MAIN)
    service.add_topic(MainTopic.ERROR)
    service.add_topic(ServiceConfig.TOPIC_NAME)
    print(f"[*] Starting Consuming {ServiceConfig.TOPIC_NAME}")
    service.start_consuming(ServiceConfig.TOPIC_NAME, callback_func=on_message_received)
