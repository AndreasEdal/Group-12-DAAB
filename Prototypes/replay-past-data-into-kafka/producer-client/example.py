#from cgi import print_directory
#from kafka import KafkaProducer
#producer = KafkaProducer(bootstrap_servers=['kafka:9092'])
#
#while True:
#    # input
#    string = str(input())
#    
#    producer.send('test2', b'Hallooooooooo')
#    # output
#    print(string)

from operator import truediv
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='localhost:9092')
exit = False
while not exit:
    inp = input()
    if(inp == "exit"):
        exit == True
        break
    producer.send('foobar',)

