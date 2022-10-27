#Código do cliente usando TCP

import random
from socket import socket, AF_INET, SOCK_STREAM
import cryptocode
import rsa
import os
from cryptography.fernet import Fernet
from math import sqrt
import time

def LimparConsole():
    os.system("cls")
 

# Função para verificar se o número é primo
def isPrime( n):
    
    if (n <= 1):
        return False
    if (n <= 3):
        return True
    if (n % 2 == 0 or n % 3 == 0):
        return False
    i = 5
    while(i * i <= n):
        if (n % i == 0 or n % (i + 2) == 0) :
            return False
        i = i + 6
    return True
 
# Função auxiliar 
def power( x, y, p):

    res = 1 
    x = x % p 
    while (y > 0):
 
        if (y & 1):
            res = (res * x) % p
 
        y = y >> 1 
        x = (x * x) % p
    return res
 
# Função para achar fatores primos
def findPrimefactors(s, n) :
 
    while (n % 2 == 0) :
        s.add(2)
        n = n // 2
 
    for i in range(3, int(sqrt(n)), 2):
         
        while (n % i == 0) :
 
            s.add(i)
            n = n // i
         
    if (n > 2) :
        s.add(n)
 
# Função para achar raiz primitiva usada na chave pública
def findPrimitive( n) :
    s = set()
 
  
    if (isPrime(n) == False):
        return -1
 
    phi = n - 1
 
    findPrimefactors(s, phi)
 
    for r in range(2, phi + 1):
 
        flag = False
        for it in s:
 
            if (power(r, phi // it, n) == 1):

                flag = True
                break

        if (flag == False):
            return r
 
    return -1
 

#Definindo cores
verdeaguab = '\033[1;36;40m'
roxo= '\033[1;35m'
vermelho= '\033[1;31m'
amarelo= '\033[1;33m'
verdeagua='\033[1;36m'
azulclarob='\033[1;34;40m'
verdeaguab='\033[1;36;40m'
verde='\033[1;32m'
brancob= '\033[1;30;40m'

# Criando o socket
Socket_Client = socket(AF_INET, SOCK_STREAM)

# Colocando o socket para realizar solicitações
Socket_Client.connect(('localhost', 13524))

# Gerando chaves públicas e privadas da biblioteca RSA para ser usada na assinatura digital e na verificação pelo servidor
(pubKey, privKey) = rsa.newkeys(512)

# Criando chaves primas e a base ou seja as chaves "p" e "g"
p = random.randint(0, 999)
while isPrime(p) == False:
    p = random.randint(0, 999)

g = findPrimitive(p)

# Enviando as chaves padrões para o servidor
Socket_Client.send((f'{p} {g}').encode())


# Recebendo resposta do servidor
resp1 = Socket_Client.recv(2048).decode()
# print(resp1)


# Gerando chave do cliente (chave A) e enviando para o servidor
valueA = random.randint(0, 999)
keyA = str((g ** valueA) % p)
Socket_Client.send(keyA.encode())


# Recebendo chave do servidor (chave B)
ChaveServidor = int(Socket_Client.recv(2048).decode())
# print(f'A chave do servidor recebida foi {ChaveServidor}')


LimparConsole()
# Gerando as chaves compartilhadas para ambos os lados
secretKey = (ChaveServidor ** valueA) % p
print(f'{brancob}>> A chave secreta comum (compartilhada) é:: {secretKey}')

# Mandando a chave compartilhada para o servidor para que tenha noção que é igual
Socket_Client.send(str(secretKey).encode())

# Recebendo chaves do servidor para comprovar que é igual
resposta = Socket_Client.recv(2048)
sameKey = resposta.decode()

# Recebendo o identificador
data = Socket_Client.recv(2048).decode()
ident = cryptocode.decrypt(data, str(secretKey))
print(ident)

# Armazenando unicamente o identificador
identificador = ident.split()
identify = identificador[-1]


# Recebendo informações sobre a região do cliente
print(f'''{azulclarob}De qual região você está mandando mensagem: 
    {roxo}[1] {verdeaguab}América do Sul
    {roxo}[2] {verdeaguab}América do Norte
    {roxo}[3] {verdeaguab}Europa 
    {roxo}[4] {verdeaguab}Ásia
    {roxo}[5] {verdeaguab}Oceania 
    {roxo}[6] {verdeaguab}África 
    {roxo}[7] {verdeaguab}Antártida 
    
    {verde}OBS: todas as regiões com exceção da AMÉRICA DO SUL (número 1) estão com acesso restrito''')

regiao = input(f'{azulclarob}Digite o número: ')

Socket_Client.send((cryptocode.encrypt(regiao, str(secretKey))).encode())

LimparConsole()

# Loop para o cliente enviar inúmeras solicitações/mensagens/arquivos
while True:
    print()
    # Mensagem que o cliente deseja enviar
    print(f'''{verdeaguab}Escolha um dos arquivos para receber: 
    {roxo}[1] {verde}Paris.jpg 
    {roxo}[2] {verde}postagem.png
    {roxo}[3] {verde}teste.pdf
    {roxo}[4] {verde}50mbfile.pdf

    {vermelho}OBS: a escrita incorreta ou o nome de um arquivo não listado irá ocasionar erro e será solicitado novamente o arquivo desejado''')
    print()
    message1 = input(f'{verdeaguab}Escreva o nome do arquivo desejado (Digite "close" para encerrar a conexão): ')
    print()
    # Verificação para fechar a conexão do cliente com o servidor
    if message1 == "close":
        message = message1 + f"|{sameKey}"

        # Mensagem Criptografada
        EncryptedMessage = cryptocode.encrypt(message, str(secretKey))

        # Enviando a mensagem pelo socket criado
        Socket_Client.send(EncryptedMessage.encode())
        
        Socket_Client.close()
        
        print("Conexão Finalizada!")
        break

    # Continuando caso deseje mandar outras requisições
    else:
        message = message1 + f"|{sameKey}"

        # Mensagem Criptografada
        EncryptedMessage = cryptocode.encrypt(message, str(secretKey))

        # Enviando a mensagem pelo socket criado
        Socket_Client.send(EncryptedMessage.encode())
        

        # Fazendo assinatura digital e enviando dados para o servidor verificar
        sign = rsa.sign(message1.encode(), privKey, 'SHA-1')
        signHex = sign.hex()

        Socket_Client.send((f'{signHex}.....{pubKey}').encode())


        ##############################################
        # Projeto 2
        
        # Continuar aqui

        # Recebendo código de erro/confirmação do servidor
        code = Socket_Client.recv(2048).decode()
        code1 = cryptocode.decrypt(code, str(secretKey))
        code = code1
        codeSplit = code.split()

        # Se o código for 200 irá receber o arquivo criptografado e descriptografar para a visualização
        if codeSplit[1] == '200':

            print(f"{verde}{code}")

            # Recebendo chave do cliente para descriptografar o arquivo que recebeu criptografado
            with open(str(identify) + '.key', 'wb') as file_chave:
                chaveArq = Socket_Client.recv(2048).decode()
                mensagem_Chave_Cliente = cryptocode.decrypt(chaveArq, str(secretKey)).encode()
                file_chave.write(mensagem_Chave_Cliente)
            
            # Abrindo a chave para descriptografar arquivos
            with open(str(identify) + '.key', 'rb') as file_chave:
                chaveArq = file_chave.read()

            # Usando a chave da biblioteca Fernet para começar descriptografar
            fernetKey = Fernet(chaveArq)

            # Recebendo arquivo criptografado
            with open(message1, 'wb') as file:
                while 1:
                    # recebendo arquivo do servidor
                    data = Socket_Client.recv(1000000)
                    if data == b'Arquivo solicitado entregue com sucesso!':
                        break
                    file.write(data)

            print(f'{verde}{message1} solicitado recebido com sucesso!\n')

            # Abrindo o arquivo criptografado
            with open(message1, 'rb') as fileEncrypt:
                encriptado = fileEncrypt.read()

            # Descriptografando o arquivo
            descriptado = fernetKey.decrypt(encriptado)

            # Abrindo o arquivo no modo de gravação e gravando os dados descriptografados no próprio arquivo (substituindo)
            with open(message1, 'wb') as fileDecrypt:
                fileDecrypt.write(descriptado)
        
        # Caso não retorne o código 200 irá gerar os erros específicos
        elif codeSplit[1] == '403':
            print(f"{amarelo}{code}")

        elif codeSplit[1] == '404':
           print(f"{vermelho}{code}")

        else:
            print(f"{azulclarob}{code}")

# COMENTÁRIOS PARA MELHORIA
# 1) ajeitar print html
# 2) como fazer gerenciamento de identificadores que sempre mudam?
# 3) organizar código
# 4) tentar otimizar??

