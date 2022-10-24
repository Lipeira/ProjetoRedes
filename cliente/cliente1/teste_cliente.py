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
 

def power( x, y, p):

    res = 1 
    x = x % p 
    while (y > 0):
 
        if (y & 1):
            res = (res * x) % p
 
        y = y >> 1 
        x = (x * x) % p
    return res
 

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
 
# Criando o socket
Socket_Client = socket(AF_INET, SOCK_STREAM)

# Colocando o socket para realizar solicitações
Socket_Client.connect(('localhost', 13524))

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
print(f'>> A chave compartilhada: {secretKey}')

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
print('''De qual região você está mandando mensagem: 
    [1] América do Sul
    [2] América do Norte
    [3] Europa 
    [4] Ásia
    [5] Oceania 
    [6] África 
    [7] Antártida 
    
    OBS: todas as regiões com exceção da AMÉRICA DO SUL (número 1) estão com acesso restrito''')

regiao = input('Digite o número: ')

Socket_Client.send((cryptocode.encrypt(regiao, str(secretKey))).encode())

LimparConsole()

# Loop para o cliente enviar inúmeras solicitações/mensagens/arquivos
while True:
    print()
    # Mensagem que o cliente deseja enviar
    print('''Escolha um dos arquivos para receber: 
    [1] Paris.jpg 
    [2] postagem.png
    [3] teste.pdf
    [4] 50mbfile.pdf

    OBS: a escrita incorreta ou o nome de um arquivo não listado irá ocasionar erro e será solicitado novamente o arquivo desejado''')
    print()
    message1 = input('Escreva o nome do arquivo desejado (Digite "close" para encerrar a conexão): ')
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

            print(code)

            # Recebendo chave do cliente para descriptografar o arquivo que recebeu criptografado
            with open(str(identify) + '.key', 'wb') as file_chave:
                chaveArq = Socket_Client.recv(2048).decode()
                msg = cryptocode.decrypt(chaveArq, str(secretKey)).encode()
                file_chave.write(msg)
            
            # Recebendo arquivo criptografado
            with open(message1, 'wb') as file:
                while 1:
                    # recebendo arquivo do servidor
                    data = Socket_Client.recv(1000000)
                    if data == b'Arquivo solicitado entregue com sucesso!':
                        break
                    file.write(data)

            print(f'{message1} recebido!\n')

            # Abrindo a chave para descriptografar arquivos
            with open(str(identify) + '.key', 'rb') as file_chave:
                chaveArq = file_chave.read()

            # Usando a chave da biblioteca Fernet para começar descriptografar
            fernetKey = Fernet(chaveArq)

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
            print(code)

        elif codeSplit[1] == '404':
           print(code)

        else:
            print(code)
