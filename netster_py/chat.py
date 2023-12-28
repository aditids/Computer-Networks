import socket
import threading
import os

def chat_server(iface: str, port: int, use_udp: bool) -> None:
    if use_udp:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host=socket.getaddrinfo(iface,port,family=socket.AF_INET)[0]
    serverSocket.bind((host[4][0],port))
    if not use_udp:
        serverSocket.listen(10)
    count = 0
    print("Hello, I am a server")
    while serverSocket:
        if use_udp:
            while True:
                message = ""
                message, address = serverSocket.recvfrom(256)
                message = message.decode('utf-8')
                if message:
                    print("got message from", address)
                    reply = ""
                    tempMsg = message.rstrip("\n")
                    if tempMsg == "hello":
                        reply = "world\n"
                    elif tempMsg == "goodbye":
                        reply = "farewell\n"
                    elif tempMsg == "exit":
                        reply = "ok\n"
                    else:
                        reply = tempMsg 
                    reply = reply.encode('utf-8')
                    serverSocket.sendto(reply, address)
                    if tempMsg == "exit":
                        serverSocket.close()
                        break
                else:
                    pass

        else:
            clientSocket, clientAddress = serverSocket.accept()
            thread = threading.Thread(target=serverTCP, args=(count, serverSocket, clientSocket, clientAddress))
            thread.start()
        count += 1

def serverTCP(count, serverSocket, clientSocket, clientAddress):

    print(f"connection {count} from {clientAddress}")
    while True:
        message = ""
        
        message = clientSocket.recv(256).decode('utf-8')
        if message:
            tempMsg = message.rstrip("\n")
            print("got message from", clientAddress)
            reply = ""
            if tempMsg == "hello":
                reply = "world\n"
            elif tempMsg == "goodbye":
                reply = "farewell\n"
            elif tempMsg == "exit":
                reply = "ok\n"
            else:
                reply = message
            reply = reply.encode('utf-8')

            clientSocket.send(reply)
            if tempMsg == "exit":
                clientSocket.close()
                serverSocket.close()
                os._exit(0)
        else:
            pass
        

def chat_client(host: str, port: int, use_udp: bool) -> None:
    
    if use_udp:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    info=socket.getaddrinfo(host,port,family=socket.AF_INET)[0]
    clientSocket.connect((info[4][0],port))

    print("Hello, I am a client")
    message = input()
    while message:
        try:
            if use_udp:
                clientSocket.sendto((message+"\n").encode('utf-8'), (info[4][0], port))
                reply, _ = clientSocket.recvfrom(256)
                reply = reply.decode('utf-8').rstrip("\n")
            else:
                clientSocket.send((message+"\n").encode('utf-8'))
                reply = clientSocket.recv(256).decode('utf-8').rstrip("\n")

            print(reply)
            tempMsg = message
            if tempMsg == "goodbye" or tempMsg == "farewell" or tempMsg == "exit":
                break

            if reply:
                message = input()
        except BrokenPipeError:
            print("Connection closed by the server.")
            break
    clientSocket.close()