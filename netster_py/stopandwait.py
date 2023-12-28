from typing import BinaryIO
import socket
import struct

def stopandwait_server(iface:str, port:int, fp:BinaryIO) -> None:

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = socket.getaddrinfo(iface, port, family=socket.AF_INET)[0]

    serverSocket.bind((host[4][0], port))

    print("Hello, I am a server")

    SequenceNumber, Acknowledgement, CurrentSequenceNumber = 0, 0, 0

    while True:
        FileToTransfer = open(fp.name, "wb")
        print("in server first while")

        while True:
            print("in server second while")

            TempData = serverSocket.recvfrom(260)
            print("data received!!!!!!!")
                
            GetDataFromClient = struct.unpack(('i' + str(len(TempData[0]) - 4) + 's'), TempData[0])
            #print(GetDataFromClient, SequenceNumber)
            print("unpacked")
            if not GetDataFromClient[1]:
                print('closing file')
                FileToTransfer.close()
                break
            print(GetDataFromClient[0],SequenceNumber)
            if GetDataFromClient[0] == SequenceNumber:
                FileToTransfer.write(GetDataFromClient[1])
                SequenceNumber += 1
                print('writing data to file')

            Acknowledgement = GetDataFromClient[0]
            CurrentSequenceNumber = SequenceNumber

            

            d = struct.pack('ii', Acknowledgement, CurrentSequenceNumber)
            print("sending")
            serverSocket.sendto(d, TempData[1])
            print("sent ack")
        
        FileToTransfer.close()
        print("Closing server socket from outer while")
        serverSocket.close()
        return

def stopandwait_client(host:str, port:int, fp:BinaryIO) -> None:
                
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 

    print("Hello, I am a client")
    SequenceNumber = 0                 
    FileToTransfer = open(fp.name,"rb")
                
    while True:

        print('reading from file')           
        TempData = FileToTransfer.read(256) 
    
        if TempData:

            while True:
                try:
                    print("in second while")
                    print('i'+str(len(TempData))+'s')

                    d = struct.pack(('i'+str(len(TempData))+'s'),SequenceNumber,TempData)
                    print("packed")
                    clientSocket.sendto(d, (host,port))
                    print("sending")
                    clientSocket.settimeout(0.06)
                    GetData = clientSocket.recvfrom(256)[0]
                    print("received ack")
                    SetData = struct.unpack('ii',GetData)
                    print("unpacked")
                    print(SetData[0],SequenceNumber)
                    if SetData[0]!=SequenceNumber:
                        continue
                    else:
                        break
                except socket.timeout:
                    continue
            SequenceNumber+=1

        else:

            print("no Data available in file, sending empty string")
            d = struct.pack(('i'+str(len(TempData))+'s'),SequenceNumber,"".encode())
            clientSocket.sendto(d, (host,port))

            break
    print("Closing file and clientsocket")
    FileToTransfer.close()
    clientSocket.close()
    return