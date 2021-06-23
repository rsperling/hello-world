# Importing the necessary modules
from netmiko import ConnectHandler

#defining the command to send to each device
command = 'show run'

class connect(object):
    #defined class and the init function contains initialization for information of virtual switched fro successful ssh connection
    def __init__(self, device_type, ip_address, port, username, password):
        self.device_type=device_type
        self.ip=ip_address
        self.port=port
        self.username=username
        self.password=password

def test(self):
    session = ConnectHandler(device_type=self.device_type, ip=self.ip, port=self.port, username=self.username,
                             password=self.password)
    output = session.send_command(command)
    print (output)


#defining information of each virtual switches like device_type,ip,username and password
if __name__ == "__main__":
    Switch0 = connect("cisco_ios", "devops-workshop.quokka.one", "2200", "root", "root")
    #sending information of each virtual device to write function for reading and comparison
    test(Switch0)