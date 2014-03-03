import imaplib
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-H", "--host", dest="host", help="hostname")
parser.add_option("-P", "--port", dest="port", default="143", help="port")
parser.add_option("-u", "--user", dest="user",help="username" )
parser.add_option("-p", "--password", dest="password", help="password")

(options, args) = parser.parse_args()

if not options.host or not options.port or not options.user or not options.password:
    print("Host/Port/User/Password missing")
    exit(1)

mail = imaplib.IMAP4(options.host,options.port)                                       
mail.login(options.user,options.password)                          
mail.select("inbox") # connect to inbox.                                        
result, data = mail.search(None, "ALL")                                         
                                                                                
ds = data[0] # data is a list.                                                  
id_list = ds.split() # ids is a space separated string                          
latest_email_id = id_list[-1] # get the latest                                  
                                                                                
result, data = mail.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID
                                                                                
raw_email = data[0][1] # here's the body, which is raw text of the whole email  
# including headers and alternate payloads                                      
                                                                                
                                                                                
print(raw_email)
