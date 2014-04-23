#!/usr/bin/env python

import socket,binascii,time,IN
from sys import exit
from optparse import OptionParser

def slicendice(msg,slices): #generator for each of the dhcp fields
    for x in slices:
        if str(type(x)) == "<type 'str'>": x=eval(x) #really dirty, deals with variable length options
        yield msg[:x]
        msg = msg[x:]

def reqparse(message): #handles either DHCPDiscover or DHCPRequest
    #using info from http://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol
    #the tables titled DHCPDISCOVER and DHCPOFFER
    data=None
    dhcpfields=[1,1,1,1,4,2,2,4,4,4,4,6,10,192,4,"msg.rfind('\xff')",1,None]
    #send: boolean as to whether to send data back, and data: data to send, if any
    #print len(message)
    hexmessage=binascii.hexlify(message)
    messagesplit=[binascii.hexlify(x) for x in slicendice(message,dhcpfields)]
    dhcpopt=messagesplit[15][:6] #hope DHCP type is first. Should be.
    if dhcpopt == '350101':
        #DHCPDiscover
        #craft DHCPOffer
        #DHCPOFFER creation:
        #options = \xcode \xlength \xdata
        lease=getlease(messagesplit[11])
        print 'Leased:',lease
        data='\x02\x01\x06\x00'+binascii.unhexlify(messagesplit[4])+'\x00\x04'
        data+='\x80\x00'+'\x00'*4+socket.inet_aton(lease)
        data+=socket.inet_aton(address)+'\x00'*4
        data+=binascii.unhexlify(messagesplit[11])+'\x00'*10+'\x00'*192
        data+='\x63\x82\x53\x63'+'\x35\x01\x02'+'\x01\x04'
        data+=socket.inet_aton(netmask)+'\x36\x04'+socket.inet_aton(address)
        data+='\x1c\x04'+socket.inet_aton(broadcast)+'\x03\x04'
        data+=socket.inet_aton(gateway)+'\x06\x04'+socket.inet_aton(dns)
        data+='\x33\x04'+binascii.unhexlify(hex(leasetime)[2:].rjust(8,'0'))
        data+='\x42'+binascii.unhexlify(hex(len(tftp))[2:].rjust(2,'0'))+tftp
        data+='\x43'+binascii.unhexlify(hex(len(pxefilename)+1)[2:].rjust(2,'0'))
        data+=pxefilename+'\x00\xff'
    elif dhcpopt == '350103':
        #DHCPRequest
        #craft DHCPACK
        data='\x02\x01\x06\x00'+binascii.unhexlify(messagesplit[4])+'\x00'*8
        data+=binascii.unhexlify(messagesplit[15][messagesplit[15].find('3204')+4:messagesplit[15].find('3204')+12])
        data+=socket.inet_aton(address)+'\x00'*4
        data+=binascii.unhexlify(messagesplit[11])+'\x00'*202
        data+='\x63\x82\x53\x63'+'\x35\x01\05'+'\x36\x04'+socket.inet_aton(address)
        data+='\x01\x04'+socket.inet_aton(netmask)+'\x03\x04'
        data+=socket.inet_aton(address)+'\x33\x04'
        data+=binascii.unhexlify(hex(leasetime)[2:].rjust(8,'0'))
        data+='\x42'+binascii.unhexlify(hex(len(tftp))[2:].rjust(2,'0'))
        data+=tftp+'\x43'+binascii.unhexlify(hex(len(pxefilename)+1)[2:].rjust(2,'0'))
        data+=pxefilename+'\x00\xff'
    return data

def release(): #release a lease after timelimit has expired
    for lease in leases:
       if not lease[1]:
          if time.time()+leasetime == leasetime:
              continue
          if lease[-1] > time.time()+leasetime:
             print "Released",lease[0]
             lease[1]=False
             lease[2]='000000000000'
             lease[3]=0

def getlease(hwaddr): #return the lease of mac address, or create if doesn't exist
   global leases
   for lease in leases:
      if hwaddr == lease[2]:
         return lease[0]
   for lease in leases:
      if not lease[1]:
         lease[1]=True
         lease[2]=hwaddr
         lease[3]=time.time()
         return lease[0]

if __name__ == "__main__":
    parser = OptionParser(description='%prog - a simple DHCP server', usage='%prog [options]')
    parser.add_option("-a", "--address", dest="address", action="store", help='server ip address (required).')
    parser.add_option("-i", "--interface", dest="interface", action="store", help='network interface to use (default all interfaces).')
    parser.add_option("-p", "--port", dest="port", action="store", help='server port to bind (default 67).')
    parser.add_option("-f", "--from", dest="offerfrom", action="store", help='ip pool from (default x.x.x.100).')
    parser.add_option("-t", "--to", dest="offerto", action="store", help='ip pool to (default x.x.x.150).')
    parser.add_option("-b", "--broadcast", dest="broadcast", action="store", help='broadcast ip to reply (x.x.x.254).')
    parser.add_option("-n", "--netmask", dest="netmask", action="store", help='netmask (default 255.255.255.0).')
    parser.add_option("-s", "--tftp", dest="tftp", action="store", help='tftp ip address (default ip address provided).')
    parser.add_option("-d", "--dns", dest="dns", action="store", help='dns ip address (default 8.8.8.8).')
    parser.add_option("-g", "--gateway", dest="gateway", action="store", help='gateway ip address (default ip address provided).')
    parser.add_option("-x", "--pxefilename", dest="pxefilename", action="store", help='pxe filename (default pxelinux.0).')

    (options, args) = parser.parse_args()

    if not (args or options.address):
        parser.print_help()
        exit(1)

    if options.interface:
        interface = options.interface
    else:
        interface = '' # Symbolic name meaning all available interfaces

    if options.port:
        port = options.port
    else:
        port = '67'
	port = int(port)

    if options.address:
        address = options.address
        elements_in_address = address.split('.')
        if len(elements_in_address) != 4:
            sys.exit(os.path.basename(__file__) + ": invalid ip address")
    else:
        exit(1)

    if options.offerfrom:
        offerfrom = options.offerfrom
    else:
        offerfrom = '.'.join(elements_in_address[0:3])
        offerfrom = offerfrom + '.100'

    if options.offerto:
        offerto = options.offerto
    else:
        offerto = '.'.join(elements_in_address[0:3])
        offerto = offerto + '.150'

    if options.broadcast:
        broadcast = options.broadcast
    else:
        broadcast = '.'.join(elements_in_address[0:3])
        broadcast = broadcast + '.254'

    if options.netmask:
        netmask = options.netmask
    else:
        netmask = '255.255.255.0'

    if options.tftp:
        tftp = options.tftp
    else:
        tftp = address

    if options.dns:
        dns = options.dns
    else:
        dns = '8.8.8.8'

    if options.gateway:
        gateway = options.gateway
    else:
        gateway = address

    if options.pxefilename:
        pxefilename = options.pxefilename
    else:
        pxefilename = 'pxelinux.0'

    leasetime=86400 #int

    leases=[]
    #next line creates the (blank) leases table. This probably isn't necessary.
    for ip in ['.'.join(elements_in_address[0:3])+'.'+str(x) for x in range(int(offerfrom[offerfrom.rfind('.')+1:]),int(offerto[offerto.rfind('.')+1:])+1)]:
        leases.append([ip,False,'000000000000',0])
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET,IN.SO_BINDTODEVICE,interface+'\0') #experimental
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(('',port))
    #s.sendto(data,(ip,port))
    
    while 1: #main loop
        try:
            message, addressf = s.recvfrom(8192)
            if not message.startswith('\x01') and not addressf[0] == '0.0.0.0':
                continue #only serve if a dhcp request
            data=reqparse(message) #handle request
            if data:
                s.sendto(data,('<broadcast>',68)) #reply
            release() #update releases table
        except KeyboardInterrupt:
            exit()
    #    except:
    #        continue
