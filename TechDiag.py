import platform
import socket
import getpass
import psutil
import os
from datetime import datetime

print("=" * 50)
print("TECHDIAG PRO")
print("=" * 50)


data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

usuario = getpass.getuser()
hostname = socket.gethostname()

try:
    ip = socket.gethostbyname(hostname)
except:
    ip = "Não identificado"

sistema = platform.system()
versao = platform.version()
arquitetura = platform.architecture()[0]
processador = platform.processor()


cpu = psutil.cpu_percent(interval=1)
ram = psutil.virtual_memory()
disco = psutil.disk_usage("C:\\")


boot = datetime.fromtimestamp(psutil.boot_time())
tempo_ligado = datetime.now() - boot


alertas = []

if cpu > 80:
    alertas.append("CPU acima de 80%")

if ram.percent > 80:
    alertas.append("RAM acima de 80%")

if disco.percent > 90:
    alertas.append("Disco acima de 90%")

if len(alertas) == 0:
    alertas.append("Nenhum alerta encontrado")


relatorio = f"""
==================================================
TECHDIAG PRO - RELATÓRIO DE DIAGNÓSTICO
==================================================

Data/Hora: {data_hora}

===== IDENTIFICAÇÃO =====

Usuário: {usuario}
Computador: {hostname}
IP Local: {ip}

===== SISTEMA =====

Sistema Operacional: {sistema}
Versão: {versao}
Arquitetura: {arquitetura}

===== HARDWARE =====

Processador: {processador}

===== TEMPO DE ATIVIDADE =====

Última Inicialização:
{boot.strftime("%d/%m/%Y %H:%M:%S")}

Tempo Ligado:
{str(tempo_ligado).split('.')[0]}

===== CPU =====

Uso Atual: {cpu}%

===== MEMÓRIA RAM =====

Total: {ram.total / (1024**3):.2f} GB
Disponível: {ram.available / (1024**3):.2f} GB
Uso: {ram.percent}%

===== DISCO =====

Total: {disco.total / (1024**3):.2f} GB
Livre: {disco.free / (1024**3):.2f} GB
Uso: {disco.percent}%

===== ALERTAS =====
"""

for alerta in alertas:
    relatorio += f"\n- {alerta}"

relatorio += """

==================================================
FIM DO RELATÓRIO
==================================================
"""


print(relatorio)

nome_arquivo = f"TechDiag_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

caminho = os.path.abspath(nome_arquivo)


with open(caminho, "w", encoding="utf-8") as arquivo:
    arquivo.write(relatorio)

print("\nRelatório salvo com sucesso!")
print(f"Arquivo: {nome_arquivo}")
print(f"Local: {caminho}")
