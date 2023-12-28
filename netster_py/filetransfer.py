from typing import BinaryIO
import socket

def file_server(iface: str, port: int, use_udp: bool, fp: BinaryIO) -> None:
    if use_udp:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = socket.getaddrinfo(iface, port, family=socket.AF_INET)[0]
    serverSocket.bind((host[4][0], port))
    if not use_udp:
        serverSocket.listen(10)

    print("Hello, I am a server")

    while True:
        ft = open(fp.name, "wb")
        print("in first while")
        try:
            # if not ft:
            #     serverSocket.close()  
            #     return  
        
            if not use_udp:
                clientSocket, cliendAddress = serverSocket.accept()
        
            while True:
                if use_udp:
                    print('reading from udp')
                    td = serverSocket.recvfrom(256)[0]
                else:
                    print('reading from tcp')
                    td = clientSocket.recv(256) 
                if len(td)==0:
                    print('breaking')
                    #ft.close()
                    #serverSocket.close()
                    #return
                    break
                print("writing data to file")
                ft.write(td)

            print('closing')
            ft.close()
            clientSocket.close()
            serverSocket.close()
            return
        except:
            ft.close()
            serverSocket.close()
            return


def file_client(host:str, port:int, use_udp:bool, fp:BinaryIO) -> None:
    if use_udp:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    info=socket.getaddrinfo(host,port,family=socket.AF_INET)[0]
    if not use_udp:   
        clientSocket.connect((info[4][0],port))
    
    print("Hello, I am a client")

    ft = open(fp.name,"rb")
    while True:
        td = ft.read(256) 
        if not td:
            #ft.close()
            break
        if use_udp:
            clientSocket.sendto(td, (host,port))
        else:
            clientSocket.send(td)
    if use_udp:
        clientSocket.sendto("".encode(), (host,port))
    else:
        clientSocket.send("".encode())

    ft.close()
    clientSocket.close()
    #return