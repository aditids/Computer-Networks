#include <stdio.h>
#include <string.h>

void send_http(char* host, char* msg, char* resp, size_t len);


/*
  Implement a program that takes a host, verb, and path and
  prints the contents of the response from the request
  represented by that request.
 */
int main(int argc, char* argv[]) {
  if (argc != 4) {
    printf("Invalid arguments - %s <host> <GET|POST> <path>\n", argv[0]);
    return -1;
  }
  char* host = argv[1];
  char* verb = argv[2];
  char* path = argv[3];

char fstr[4096];
char arr[] = "HTTP/1.0\r\n";
char delimiter[] = "\r\n\r\n";
char response[4096];

strcat(fstr, verb);
strcat(fstr, " ");
strcat(fstr, path);
strcat(fstr, " ");
strcat(fstr, arr);
strcat(fstr, "Host: ");
strcat(fstr, host);
strcat(fstr, delimiter);

if(strcmp(verb,"POST")==0){
  char length_of_content[]="Content-Length:10\r\n";
  strcat(fstr,length_of_content);
  send_http(host, fstr, response, 4096);
}
else{
  send_http(host, fstr, response, 4096);
}
printf("%s\n", response);
  return 0;
}
