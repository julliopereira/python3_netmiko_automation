
import platform

def ping(host):
    import os, platform

    if  platform.system().lower()=="windows":
        ping_str = "-n 1"
    else:
        ping_str = "-c 1"

    resposta = os.system("ping " + ping_str + " " + host)
    return resposta == 0

p = ping('8.8.8.8')

print(platform.system())

if p == 0:
    print('ping ok')
else:
    print('ping nok')