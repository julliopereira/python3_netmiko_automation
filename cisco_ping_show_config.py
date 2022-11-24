#from netmiko import ConnectHandler
import os 
import time
from netmiko import ConnectHandler

def ping_dev(ip):
    # Pinga dispositivo e grava status na variavel res
    res = os.system(f"ping -c 1 {ip} -i 0.2 -W 0.3 > /dev/null ; echo $?")
    return res

def cisco_show(ip):
    # Mostrar comando show ip interface brief
    cisco = { 
        'device_type': 'cisco_ios',
        'host': ip,
        'username': 'cisco',
        'password': 'cisco',
        'port': '22',
        'secret': 'cisco'
    }
    connect = ConnectHandler(**cisco)
    cisco_command = "show ip interface brief"

    output = connect.send_command(cisco_command)
    #time.sleep(2)
    print(output)

def cisco_config(ip):
    # Configuração de hostname loggin buffered e no loggin console
    cisco = { 
        'device_type': 'cisco_ios',
        'host': ip,
        'username': 'cisco',
        'password': 'cisco',
        'port': '22',
        'secret': 'cisco'
    }
    connect = ConnectHandler(**cisco)

    config_commands = [ "hostname router_" + ip,
                    'logging buffered 20010',
                    'no logging console' ]

    output = connect.send_config_set(config_commands)
    #time.sleep(2)
    print(output)

# Ler arquivo e gravar em lista
with open("devices.txt", "r") as arquivo:
    ips = arquivo.readlines()

# Para cada valor da lista 
for ip in ips:
    ip = ip.rstrip('\n')
    val = ping_dev(ip)
    # Se pingar então 
    if val == 0:
        cisco_show(ip)
        cisco_config(ip)


