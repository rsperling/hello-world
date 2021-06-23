# libs/modules
import configparser
import difflib
import time
import smtplib
import yaml

from datetime import datetime
from configparser import ExtendedInterpolation
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from netmiko import ConnectHandler


# owned
__author__ = 'Rich Bocchinfuso'
__copyright__ = 'Copyright 2021, Sample switch config diff reporter for DevOps Workshop'
__credits__ = ['Rich Bocchinfuso']

__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = 'Rich Bocchinfuso'
__email__ = 'rbocchinfuso@gmail.com'
__status__ = 'Dev'

# read config paramaters from config.ini file using configparser

# prepare the config file reference
CONFIG = configparser.ConfigParser(interpolation=ExtendedInterpolation())
CONFIG.read('./config.ini')

# prepare SMTP-related variables from the config file
SMTP_SERVER = CONFIG['SMTP Info']['server']
SMTP_PORT = CONFIG['SMTP Info']['port']
SMTP_USERNAME = CONFIG['SMTP Info']['username']
SMTP_PASSWORD = CONFIG['SMTP Info']['password']

# prepare mailer variable from the config file
FROM = CONFIG['Mailer Info']['from']
TO = CONFIG['Mailer Info']['to']
CC = CONFIG['Mailer Info']['cc']
BCC = CONFIG['Mailer Info']['bcc']
ALL = TO + ',' + CC + BCC

# prepare message content variables from the config file
SUBJECT = CONFIG['Message Info']['subject']


# defining the command to send to each device
command = 'show run'


class read_from_files(object):
    # defined class and the init function contains initialization for information of virtual switched from successful ssh connection
    def __init__(self, name, device_type, ip_address, port, username, password):
        self.name = name
        self.device_type = device_type
        self.ip = ip_address
        self.port = port
        self.username = username
        self.password = password

    # defining write function to read configuration information of network devices from yesterday's date and today's date and compare those two files
    def write_fromfile(self):
        # establishing session to connect to device using SSH
        session = ConnectHandler(device_type=self.device_type, ip=self.ip, port=self.port, username=self.username,
                                 password=self.password)
        # entering the session
        enable = session.enable()
        # sending commmand and storing output
        output = session.send_command(command)

        # ### daily comparison code
        # #defining the file from yesterday, for comparison
        # old_configfile = '/code/configfiles/' + self.ip + '_' + self.port + '_' + (
        #     datetime.date.today() - datetime.timedelta(days=1)).isoformat()
        # #writing the command to a file for today
        # with open('/code/configfiles/' + self.ip + '_' + self.port + '_' + datetime.date.today().isoformat(), 'w') as new_configfile:
        #     new_configfile.write(output + '\n')
        # #extracting differences between yesterday's and todays file in HTML format
        # with open(old_configfile, 'r') as old_file, open(
        #     '/code/configfiles/' + self.ip + '_' + self.port + '_' + datetime.date.today().isoformat(),
        #     'r') as new_file:
        #     compare = difflib.HtmlDiff().make_file(fromlines=old_file.readlines(), tolines=new_file.readlines(),
        #                                        fromdesc=(datetime.date.today() - datetime.timedelta(
        #                                            days=1)).isoformat(),
        #                                        todesc=datetime.date.today().isoformat())
        #     #sending differences to mail function for forwarding as email
        #     # read_from_files.toscreen(compare)
        #     read_from_files.mail(compare)

        # basline comparison code
        # defining baseline, for comparison
        baseline_configfile = '/code/configfiles/baseline.txt'
        # writing current config
        with open('/code/configfiles/' + self.ip + '_' + self.port, 'w') as current_configfile:
            current_configfile.write(output + '\n')
        # extracting differences between basline and current config file in HTML format
        with open(baseline_configfile, 'r') as baseline_file, open(
            '/code/configfiles/' + self.ip + '_' + self.port,
                'r') as current_file:
            compare = difflib.HtmlDiff().make_file(fromlines=baseline_file.readlines(), tolines=current_file.readlines(),
                                                   fromdesc=(
                                                       'Baseline Config'),
                                                   todesc=datetime.now().isoformat())
            # sending differences to mail function for forwarding as email
            # read_from_files.toscreen(compare)
            read_from_files.mail(name,compare)

    # defining function for sending comparison report to screen
    # def toscreen(compare):
    #     print (compare)

    # defining function for sending comparison report via email

    def mail(name,compare):
        msg = MIMEMultipart()
        msg['From'] = FROM
        msg['To'] = TO
        msg['Subject'] = name + ': ' + SUBJECT
        msg.attach(MIMEText(compare, 'html'))
        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(FROM, TO, msg.as_string())
            server.quit()
            print("email report sent successfully")
        except Exception as e:
            print(e)
            print('something went wrong...')


# defining information of each virtual switches like device_type,ip,username and password
if __name__ == "__main__":
    while(True):
        # read switch config details from switches.yml using PyYAML
        f = open('switches.yml')
        switch_yaml = yaml.safe_load(f)
        f.close()

        for switch_id in switch_yaml['switches']:
            name = switch_yaml['switches'][switch_id]['name']
            type = switch_yaml['switches'][switch_id]['type']
            address = switch_yaml['switches'][switch_id]['address']
            port = switch_yaml['switches'][switch_id]['port']
            username = switch_yaml['switches'][switch_id]['username']
            password = switch_yaml['switches'][switch_id]['password']
            switch = read_from_files(
                str(name), str(type), str(address), str(port), str(username), str(password))
            # sending information of each virtual device to write function for reading and comparison
            read_from_files.write_fromfile(switch)

        time.sleep(60)
