import socket
import picar_4wd as fc
from gpiozero import CPUTemperature
import time

HOST = "192.168.3.14" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

def interpret_cmd(client, cmd):
    if (cmd == b"38") or (cmd == b"forward"):
        print(cmd)
        fc.forward(30)
        time.sleep(0.3)
        fc.stop()
        client.sendall(cmd) # Echo back to client

    if (cmd == b"40") or (cmd == b"backward"):
        print(cmd)
        fc.backward(30)
        time.sleep(0.3)
        fc.stop()
        client.sendall(cmd) # Echo back to client

    if (cmd == b"37") or (cmd == b"left"):
        print(cmd)
        fc.turn_left(30)
        time.sleep(0.3)
        fc.stop()
        client.sendall(cmd) # Echo back to client

    if (cmd == b"39") or (cmd == b"right"):
        print(cmd)
        fc.turn_right(30)
        time.sleep(0.3)
        fc.stop()
        client.sendall(cmd) # Echo back to client
    
    if (cmd == b"temperature"):
        print(cmd)
        cpu = CPUTemperature()
        response = "temperature" + str(cpu.temperature)
        print(response)
        client.sendall(response.encode())




with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            cmd = client.recv(1024)      # receive 1024 Bytes of message in binary format
            if cmd != b"":
                #print(cmd)     
                interpret_cmd(client, cmd)
                
                
    except: 
        print("Closing socket")
        client.close()
        s.close()    

