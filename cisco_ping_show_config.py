#from netmiko import ConnectHandler
import os
import time

def ping_dev(ip):
    # Pinga dispositivo e grava status na variavel res
    res = os.system(f"ping -c 1 {ip} -i 0.2 -W 0.3 > /dev/null ; echo $?")
    return res

def cisco_config(ip):
    # Configuração de hostname
    cisco = { 
        'device_type': 'cisco_ios',
        'host': ip,
        'username': 'cisco',
        'password': 'cisco',
        'port': '22',
        'secret': 'cisco'
    }
    print(cisco)

# Ler arquivo e gravar em lista
with open("devices.txt", "r") as arquivo:
    ip = arquivo.readlines()

# Para cada valor da lista 
for ip in ip:
    ip = ip.rstrip('\n')
    val = ping_dev(ip)
    # Se pingar então configura hostname
    if val == 0:
        cisco_config(ip)
        time.sleep(2)


