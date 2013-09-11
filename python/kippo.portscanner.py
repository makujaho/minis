# Cycles through servers with ssh to execute one command on each machine
# can be used to write a simple cluster shell oder similar

import paramiko

server = [
    {'host': 'unikorn.me','port':22,'user':'root','password':'123456'},
]
command = 'wget 217.145.98.122:564'


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

out = []
for i in server:
    ssh.connect(i['host'],port=i['port'], username=i['user'], password=i['password'])
    stdin, stdout, stderr = ssh.exec_command(command)
    print stderr
    print stdout
    out += [stdout.readlines()[0][:-1]]
    #ssh.shutdown(2)
print out
