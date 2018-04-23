import pika
import sqlite3


def callback(ch, method, properties, body):
    # Парсим полученную строку
    string = body.decode('ascii')
    a = string.split('/')[0]
    b = int(string.split('/')[1])
    c = int(string.split('/')[2])
    d = string.split('/')[3]
    print(str(a) + " " + str(b) + " " + str(c)+" "+str(d))
    # Подключаемся к БД и обновляем результат
    sqlite_file = 'D:\CloudProject\App\db.sqlite3'
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    params = (str(a),str(d))
    sql = "UPDATE webinterface_object SET status=? WHERE id=?"
    cursor.execute(sql,params)
    conn.commit()

    print('Succesfully updated')



connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='results')
channel.basic_consume(callback,
                      queue='results',
                      no_ack=True)
channel.start_consuming()