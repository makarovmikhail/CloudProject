from _thread import start_new_thread
import pika
import time

from HoltWinters import triple_exponential_smoothing
from CrossValidation import timeseriesCVcore
from CrossValidation import set_global_n
from scipy.optimize import minimize

from data import series
from data import slen
from data import n_predicts


def callback(ch, method, properties, body):
    string = body.decode('ascii')
    a = string.split(' ')[0]
    b = int(string.split(' ')[1])
    c = int(string.split(' ')[2])
    print('Recieved: '+string)
    set_global_n(c)
    start_new_thread(startcompute,(a,b,c,))


def startcompute(id,n_pred,n_spli):
    time.sleep(10)
    opt = minimize(timeseriesCVcore, x0=[0,0,0], method="TNC", bounds=((0, 1), (0, 1), (0, 1)))
    alpha_final, beta_final, gamma_final = opt.x
    print(alpha_final, beta_final, gamma_final)
    result = triple_exponential_smoothing(series, slen, alpha_final, beta_final, gamma_final, n_predicts)
    # Вывод последних значений в количестве n_predicts
    print(result[-n_predicts:])
    # Отправим результат
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='results')
    channel.basic_publish(exchange='',
                          routing_key='results',
                          body=str(id)+"/"+str(n_pred) + "/" + str(n_spli)+"/"+str(result[-n_predicts:]))
    print('Sending results...')
    connection.close()



connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')
channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)
channel.start_consuming()
