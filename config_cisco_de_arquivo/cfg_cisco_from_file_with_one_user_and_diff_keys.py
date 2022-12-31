# AUTHOR        : JULIO C. PEREIRA
# CONTATO       : julliopereira@gmail.com
# OBJETIVO      : CONFIGURAR VÁRIOS EQUIPAMENTOS AUTOMATICAMENTE
#                 UTILIZANDO PROTOCOLO SSH 
#

# <<IMPORTANTE>> ANTES DE RODAR O PROGRAMA:
#   - Tenha certeza que o arquivo comandos.txt é presente no diretório e com comandos a serem aplicados
#   - Tenha certeza que o arquivo devices.txt é presente no diretório e com os ips dos equipamentos 
#   - Tenha certeza que o arquivo noping.txt é presente no diretório 
#   - Tenha certeza que o arquivo configured.txt é presente no diretório 
#   - Tenha certeza que os modulos netmiko e termcolor estão instalados
#       - pip install netmiko
#       - pip install termcolor
#



#from netmiko import ConnectHandler
import os 
import time
from netmiko import ConnectHandler
import datetime
from termcolor import colored
import subprocess

def ping_dev(ip):
    # Pinga dispositivo e grava status na variavel res
    res = subprocess.run(["ping","-c","1","-i","0.2","-W","0.3", ip], capture_output=True)
    return res

def cisco_config(ip,username,password,data):
    # Configura o equipamento
    cisco = {
          'device_type': 'cisco_ios',
         'host': ip,
          'username': username,
          'password': password,
          'port': '22',
          'secret': 'cisco'
    }
    connect = ConnectHandler(**cisco)
    output = connect.send_config_from_file("comandos.txt")

    print(f"{output} \n")
    connect.disconnect() # TALVEZ REMOVER OU COMENTAR LINHA
 
    with open('configured.txt', 'a') as cfg:
        # Mostra na tela resultado da configuracao
        cfg.write("-"*10 + str(data) + "-"*10 + " username: " + str(username) + " -- IP: " + str(ip) + "\n")
        cfg.write(f"{output} \n")
    

# Ler arquivo e gravar em lista
with open("devices.txt", "r") as arquivo:
    ips = arquivo.readlines()

#coletar username uma unica vez
username = str(input("username: "))
# Para cada valor da lista 
for ip in ips:
    # Coletar password para cada equipamento
    print(f"{'-'*80} {ip}")
    password = str(input(colored("password: ", "red")))
    
    data = datetime.datetime.now() 

    ip = ip.rstrip('\n')
    val= ping_dev(ip)
    
    if val.returncode == 0:
        # Se pingar então 
        cisco_config(ip,username,password,data)
    else:
        # Se nao pingar então 
        print("Dispositivo não acessível ...\n")
        with open('noping.txt','a') as nping:
            nping.write(f"{ip} \t {data} no icmp connection")


