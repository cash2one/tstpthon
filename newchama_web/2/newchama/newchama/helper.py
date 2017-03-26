#encoding:utf-8
import pika
import pickle
from newchama.settings import EMAIL_HOST_USER,IS_PRODUCT_HOST

def send_email_by_mq(queue,routing_key,title,email,html_content):
    if IS_PRODUCT_HOST:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                   'localhost'))
    else:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                   'test.newchama.com'))
    channel = connection.channel()
    channel.queue_declare(queue=queue)

    c={}
    c['title']=title
    c['email']=email
    c['content']=html_content

    channel.basic_publish(exchange='', routing_key=routing_key, body=pickle.dumps(c))
    channel.close()
    connection.close()


def send_email_by_mq_multiple(queue,routing_key,title,email_list,html_content_list):
    if IS_PRODUCT_HOST:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                   'localhost'))
    else:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                   'test.newchama.com'))
    channel = connection.channel()
    channel.queue_declare(queue=queue)

    for item in zip(email_list,html_content_list):

        c={}
        c['title']=title
        c['email']=item[0]
        c['content']=item[1]

        channel.basic_publish(exchange='', routing_key=routing_key, body=pickle.dumps(c))
    channel.close()
    connection.close()
