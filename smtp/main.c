#include <stdio.h>
#include <string.h>

int connect_smtp(const char* host, int port);
void send_smtp(int sock, const char* msg, char* resp, size_t len);



/*
  Use the provided 'connect_smtp' and 'send_smtp' functions
  to connect to the "lunar.open.sice.indian.edu" smtp relay
  and send the commands to write emails as described in the
  assignment wiki.
 */
int main(int argc, char* argv[]) {
  if (argc != 3) {
    printf("Invalid arguments - %s <email-to> <email-filepath>", argv[0]);
    return -1;
  }

  char* rcpt = argv[1];
  char* filepath = argv[2];

  int socket = connect_smtp("lunar.open.sice.indiana.edu", 25); 

  char temp_string[150];
  char response[4096];
  char text[1024];

  FILE *FilePointer = fopen(filepath,"r");
  if(FilePointer!=NULL)
  {
    while(fgets(temp_string,150,FilePointer))
    {
      strcat(text, temp_string);
    }
  }
  char* message = strcat(text,"\r\n.\r\n");
  char Crcpt[150] = "RCPT TO:<";
  char Cmail[150] = "MAIL FROM:<";
  char *rstr = strcat(Crcpt,rcpt);
  char *mstr = strcat(Cmail,rcpt);
  char endl[]=">\n";
  mstr = strcat(mstr,endl);
  rstr = strcat(rstr,endl);
  send_smtp(socket, "HELO iu.edu\n", response, 4096);
  printf("%s\n", response); 
  send_smtp(socket, mstr, response, 4096);
  printf("%s\n", response); 
  send_smtp(socket, rstr, response, 4096);
  printf("%s\n", response); 
  send_smtp(socket, "DATA\n", response, 4096);
  printf("%s\n", response);
  send_smtp(socket, message, response, 4096);
  printf("%s\n", response);

  send_smtp(socket,"QUIT\r\n", response, 4096);
  return 0;
}