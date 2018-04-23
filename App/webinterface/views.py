from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

import pika
from _thread import start_new_thread

from .models import Object


def callback(ch, method, properties, body):
    # Парсим полученную строку
    string = body.decode('ascii')
    a = string.split('/')[0]
    b = int(string.split('/')[1])
    c = int(string.split('/')[2])
    d = string.split('/')[3]
    print(str(a)+" "+str(b)+" "+str(c))
    # Обновляем запись в БД
    obj = Object.objects.get(id=a)
    obj.status = d
    obj.save()


def startupdate():
    # Проверяем есть ли результаты
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='results')
    channel.basic_consume(callback,
                          queue='results',
                          no_ack=True)
    channel.start_consuming()
    connection.close()


def index(request):
    latest_task_list = Object.objects.order_by('-id')[:10]
    context = {'latest_object_list': latest_task_list, 'predict_list': range(1,8), 'split_list':range(3,15)}
    start_new_thread(startupdate,())
    return render(request, 'webinterface/index.html', context)

def addtask(request):
    try:
        obj = Object(n_predicts=int(request.POST['n_predicts']), n_splits=int(request.POST['n_splits']), status="Waiting...")
        isComputed = False
        for item in Object.objects.all():
            if item.n_predicts == obj.n_predicts and item.n_splits == obj.n_splits and item.status != "Waiting..." :
                obj.status = item.status
                isComputed = True
                break
        obj.save()
        if not isComputed:
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()
            channel.queue_declare(queue='hello')
            channel.basic_publish(exchange='',
                                  routing_key='hello',
                                  body=str(obj.id)+" "+str(obj.n_predicts)+" "+str(obj.n_splits))
            connection.close()
    except:
        return HttpResponseRedirect(reverse('webinterface:index'))
    return HttpResponseRedirect(reverse('webinterface:index'))