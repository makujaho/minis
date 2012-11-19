#!/usr/bin/python

import socket
import sys

def main(dest_name):
    dest_addr = socket.gethostbyname(dest_name)
    last_addr = None
    port = 33434
    max_hops = 30
    icmp = socket.getprotobyname('icmp')
    udp = socket.getprotobyname('udp')
    ttl = 1
    while True:
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
        send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        recv_socket.bind(("", port))
        send_socket.sendto("", (dest_name, port))
        curr_addr = None
        curr_name = None
        try:
            _, curr_addr = recv_socket.recvfrom(512)
            curr_addr = curr_addr[0]
            try:
                curr_name = socket.gethostbyaddr(curr_addr)[0]
            except socket.error:
                curr_name = curr_addr
        except socket.error:
            pass
        finally:
            send_socket.close()
            recv_socket.close()

        curr_host = "%s (%s)" % (curr_name, curr_addr) if curr_addr is not None else "*"
        print "%d\t%s" % (ttl, curr_host)

        ttl += 1
        if curr_addr == dest_addr or last_addr == cur_addr or ttl >= max_hops:
            break
        last_addr = curr_addr

if __name__ == "__main__":
    main(sys.argv[1])
