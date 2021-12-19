#APP UpFile 1.0
#Aplicativo que verificará a cada três minutos uma pasta num diretório da rede. Caso seja .zip, ele subirá para o FTP e devolverá um arquivo .txt contendo o link para download.

#Importa as bibliotecas necessárias para funcionamento (requirements.txt)
import ftplib
import os
import glob
from time import sleep
from datetime import datetime

#Cria a lista arquivos
arquivos = list()

#Função para fazer o upload dos arquivos
def upload(f):
    session = ftplib.FTP('ENDEREÇODOFTP','LOGINDOFTP', 'SENHA')
    file = open(f,'rb')
    session.cwd('/www/DIRETORIOUPLOAD')
    ftplib.FTP.port=22
    session.storbinary(f'STOR {f}', file)
    file.close()
    session.quit()
    os.remove(f"{f}")

#Função para registrar no arquivo links.txt os links que foram gerados após o upload
def arquivotxt(f):
    d = datetime.today().strftime('%Y-%m-%d')
    h = datetime.today().strftime('%H:%M')
    arquivotxt = open('links.txt', 'a')
    arquivotxt.write('-='*30)
    arquivotxt.write(f'\nArquivo: {f} \n')
    arquivotxt.write(f'Upload feito em {d} às {h}.  \n')
    arquivotxt.write(f'Link para download: www.SEUDOMINIO.com.br/download/{f}\n\n')
    print(f'{h} --= Upload do arquivo {f} realizado com sucesso! =--')
    arquivotxt.close()

#Aqui ele verificará a cada 60 segundos se tem arquivos nogos no diretorio para subir para o FTP.
while True:
    hora = datetime.today().strftime('%H:%M')
    #pasta = './arquivos'
    for file in glob.glob('*.zip'):
        arquivos.append(file)
    for file in glob.glob('*.rar'):
        arquivos.append(file)
    for c in range(len(arquivos)):
        #print(c)
        upload(arquivos[c])
        arquivotxt(arquivos[c])
        c += 1
    #Mensagem de standby.
    print(f'{hora} --= Standby. Aguardando arquivos. ==-')
    #Precisamos limpar a lista arquivos para ela não procurar novamente um arquivo que já subiu.
    arquivos.clear()
    #Espera a próxima leva de arquivos em segundos.
    sleep(60)