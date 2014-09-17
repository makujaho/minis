import socket
import sys

if len(sys.argv) < 3:
    print "Usage: ",sys.argv[0]," <host> <port>[,<port>,<port>]"
    exit(1)

for i in sys.argv[2].split(','):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((sys.argv[1],int(i)))

    print i,(" O" if not result else " X")
