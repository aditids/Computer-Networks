#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>

/*
  Use the `getaddrinfo` and `inet_ntop` functions to convert a string host and
  integer port into a string dotted ip address and port.
 */
int main(int argc, char* argv[]) {
  if (argc != 3) {
    printf("Invalid arguments - %s <host> <port>", argv[0]);
    return -1;
  }
  char* host = argv[1];
  char* port = argv[2];
  struct addrinfo hints;
  struct addrinfo *res, *resptr;
  hints.ai_family = PF_UNSPEC;
  hints.ai_socktype = SOCK_STREAM;
  hints.ai_protocol = IPPROTO_TCP;
  hints.ai_flags = AI_PASSIVE;

  char buffer[INET6_ADDRSTRLEN];
  int s;
  s = getaddrinfo(host,port,&hints,&res);
  if (s != 0) 
  {
    fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(s));
    exit(EXIT_FAILURE);
  }
  for(resptr = res; resptr!=NULL; resptr=resptr->ai_next)
  {
    void* raw_addr;
    if (resptr->ai_family == AF_INET) // Address is IPv4
    { 
      struct sockaddr_in* tmp = (struct sockaddr_in*)resptr->ai_addr; 
      raw_addr = &(tmp->sin_addr);
      inet_ntop(AF_INET,raw_addr,buffer, sizeof(buffer));
      printf("IPv4 %s\n", buffer);
    }
    else // Address is IPv6
    { 
      struct sockaddr_in6* tmp = (struct sockaddr_in6*)resptr->ai_addr; 
      raw_addr = &(tmp->sin6_addr); 
      inet_ntop(AF_INET6,raw_addr,buffer, sizeof(buffer));
      printf("IPv6 %s\n", buffer);
    }
  }
  return 0;
}