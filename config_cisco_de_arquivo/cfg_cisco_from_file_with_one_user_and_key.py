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
import subprocess


#### definicao de variaveis

COMANDOS = "comandos.txt"
CONFIGURADOS = "configured.txt"
DISPOSITIVOS = "devices.txt"
NOPING = "noping.txt"

####


def ping_dev(ip):
    # Pinga dispositivo e grava status na variavel res
    res = subprocess.run(["ping","-c","1","-i","0.2","-W","0.3", ip], capture_output=True)
    return res


def cisco_config(ip,username,password,data):
    # Acessa equipamento e aplica configuracao
    cisco = {
          'device_type': 'cisco_ios',
          'host': ip,
          'username': username,
          'password': password,
          'port': '22',
          'secret': 'cisco'
    }
    connect = ConnectHandler(**cisco)
    output = connect.send_config_from_file(COMANDOS)

    print(f"{output} \n")
    connect.disconnect() 
  
    with open(CONFIGURADOS, 'a') as cfg:
        # Mostra na tela uma resumo do que foi aplicado
        cfg.write("-"*10 + str(data) + "-"*10 + " username: " + str(username) + " -- IP: " + str(ip) + "\n")
        cfg.write(f"{output} \n")
        
# Ler arquivo e gravar em lista
with open(DISPOSITIVOS, "r") as arquivo:
    ips = arquivo.readlines()

# Coletar credenciais
username = str(input("username: "))
password = str(input("password: "))
# Para cada valor da lista 
for ip in ips:
    print(f"{'-'*80} {ip}") # linha
    # Armazena informacao de data/hora atual
    data = datetime.datetime.now() 
    # remove \n no final da linha de cada ip
    ip = ip.rstrip('\n')
    # faz teste de ping usando a funcao ping_dev
    val= ping_dev(ip)
    # realiza configuracao se houve conectividade
    if val.returncode == 0:
        # Se pingar então configura
        cisco_config(ip,username,password,data)
    else:
        # Se nao pingar então grave resultado negativo em arquivo
        print("Dispositivo não acessível ...\n")
        with open(NOPING,'a') as nping:
            nping.write(f"{ip} \t {data} no icmp connection")


