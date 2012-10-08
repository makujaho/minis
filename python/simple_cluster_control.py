# Cycles through servers with ssh to execute one command on each machine
# can be used to write a simple cluster shell oder similar

import paramiko

server = [
    {'host': '','port':22,'user':'','password':''},
]
command = 'date +%s'


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

out = []
for i in server:
    ssh.connect(i['host'],port=i['port'], username=i['user'], password=i['password'])
    stdin, stdout, stderr = ssh.exec_command(command)
    out += [stdout.readlines()[0][:-1]]
    #ssh.shutdown(2)

print ';'.join(out)
