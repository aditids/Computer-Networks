from typing import BinaryIO
import socket
import pickle

def gbn_server(iface:str, port:int, fp:BinaryIO) -> None:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = socket.getaddrinfo(iface, port, family=socket.AF_INET)[0]
    serverSocket.bind((host[4][0], port))

    print("Hello, I am a server")

    FileToTransfer = open(fp.name, "wb")
    SequenceNumber, Acknowledgement, CurrentSequenceNumber = 0, 0, 0

    while True:
        try:
            print("receiving..")

            TempData = serverSocket.recvfrom(1024)
            GetData = pickle.loads(TempData[0])

            # if GetData:
            #     serverSocket.settimeout(0.06)
            
            print(GetData[0], SequenceNumber)
            if GetData[0] == SequenceNumber:
                if GetData[1]:
                    print("writing...")
                    FileToTransfer.write(GetData[1])
                    Acknowledgement = SequenceNumber
                    SequenceNumber+=1
                else:
                    print("no data")
                    FileToTransfer.close()
                    serverSocket.close()
                    return
                    #break
                
                #packet = [2,SequenceNumber]
                
                # print("sending ack", Acknowledgement)
                # serverSocket.sendto(pickle.dumps(Acknowledgement),TempData[1])
            else:
                print("packet lost", SequenceNumber) 
                             
                Acknowledgement = SequenceNumber-1
                #serverSocket.sendto(pickle.dumps(Acknowledgement),TempData[1])
            print("sending ack", Acknowledgement)
            serverSocket.sendto(pickle.dumps(Acknowledgement),TempData[1])
        except:
            print("breaking from exception..")
            break

    print("closing...")
    FileToTransfer.close()
    serverSocket.close()
    return

def gbn_client(host:str, port:int, fp:BinaryIO) -> None:
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    info=socket.getaddrinfo(host,port,family=socket.AF_INET)[0]
    serverConnection = (info[4][0],port) 
    print("Hello, I am a client")
                   
    FileToTransfer = open(fp.name,"rb")

    SequenceNumber = 0  
    init = 0
    maxsize = 4
    #flag = 1
    gbnWindow = []

    TempData = FileToTransfer.read(256) 

    WindowSize = 4

    while TempData or gbnWindow:
        print("Seq -",SequenceNumber," init -", init," WindowSize - ", WindowSize)
        while TempData and SequenceNumber < init+WindowSize:
            # if not TempData:
            #     print("no data")
            #     flag=0

            packet = [SequenceNumber, TempData]

            print("sending data to server")
            clientSocket.sendto(pickle.dumps(packet,protocol=pickle.DEFAULT_PROTOCOL),serverConnection)

            #clientSocket.settimeout(0.06)

            SequenceNumber+=1
            gbnWindow.append(packet)
            TempData = FileToTransfer.read(256)
            print("reading again")
            #clientSocket.settimeout(0.06)

        flag = 0
        while not flag:
            try:
                clientSocket.settimeout(0.005)
                td = clientSocket.recvfrom(1024)
                
                k = pickle.loads(td[0])
                print("response - ", k, " init - ",init)
                if k >= init:
                    #lastAck = time.time()
                    init=1+k
                    #print(gbnWindow)
                    while gbnWindow and gbnWindow[0][0]<=k:
                        gbnWindow.pop(0)
                    WindowSize += 1


            except socket.timeout:
                print("in except decreasing WindowSize..")
                WindowSize = max(WindowSize // 2, 1)
                for i in gbnWindow:
                    clientSocket.sendto(pickle.dumps(i),serverConnection)                
                break
    
    print("closing...")
    clientSocket.sendto(pickle.dumps([SequenceNumber,"".encode()]),serverConnection)
    FileToTransfer.close()
    clientSocket.close()
    return