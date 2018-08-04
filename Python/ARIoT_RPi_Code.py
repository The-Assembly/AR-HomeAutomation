import socket
import RPi.GPIO as GPIO
from time import sleep

light = -1
ac = -1
door = -1

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


GPIO.setup(3, GPIO.OUT)
GPIO.output(3, 0)
GPIO.setup(5, GPIO.OUT)
pwm = GPIO.PWM(5,50)
pwm.start(0)

def setAngle(angle):
        duty = angle/18 +2
        GPIO.output(5,True)
        pwm.ChangeDutyCycle(duty)
        sleep(1)
        GPIO.output(5,False)
        pwm.ChangeDutyCycle(0)

while 1:    
        store = []
        backlog=1
        size = 1024
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("10.4.138.77",50001))   #IMPORTANT: change the ip address to match the one printed on the back of the raspberry pi
        s.listen(backlog)
        try:
            print ( "Waiting...")
            client, address = s.accept()

            while 1:
                data = client.recv(size)
                if data:
                    tabela = data.decode('ascii')
                    print ( "Received Data :")
                    print (tabela)
                    print(data)
                    client.send(data)
                    if tabela == "Toggle Lights Status":
                        light = -light
                        if light == 1:
                            GPIO.output(3, 1)
                        else:
                            GPIO.output(3, 0) 
                    elif tabela == "Toggle AC Status":
                        ac = -ac
                    elif tabela == "Toggle Door Status":
                        door = -door
                        if door == -1:
                            setAngle(0)
                        else:
                            setAngle(180)
                        

                    
        except Exception as e:
            print(e)
            print("closing socket")
            client.close()
            s.close()
