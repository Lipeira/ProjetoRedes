#Código do cliente usando TCP

import random
from socket import socket, AF_INET, SOCK_STREAM
import raizesPrimitivas2
import cryptocode
import rsa
import os
from cryptography.fernet import Fernet
import time

# Criando o socket
Socket_Client = socket(AF_INET, SOCK_STREAM)

# Colocando o socket para realizar solicitações
Socket_Client.connect(('localhost', 13524))

(pubKey, privKey) = rsa.newkeys(512)

# Criando chaves primas e a base ou seja as chaves "p" e "g"
p = random.randint(0, 999)
while raizesPrimitivas2.isPrime(p) == False:
    p = random.randint(0, 999)

g = raizesPrimitivas2.findPrimitive(p)

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


# Gerando as chaves compartilhadas para ambos os lados
secretKey = (ChaveServidor ** valueA) % p
print(f'>> A chave compartilhada: {secretKey}')

# Mandando a chave compartilhada para o servidor para que tenha noção que é igual
Socket_Client.send(str(secretKey).encode())

# Recebendo chaves do servidor para comprovar que é igual
resposta = Socket_Client.recv(2048)
sameKey = resposta.decode()

# Recebendo o identificador
data = Socket_Client.recv(2048)
ident = data.decode()
print(ident)

# Loop para o cliente enviar inúmeras solicitações/mensagens/arquivos
while True:
    # Mensagem que o cliente deseja enviar
    message1 = input('>> Escreva a mensagem (Digite "close" para encerrar a conexão): ')

    if message1 == "close":
        message = message1 + f"|{sameKey}"

        # Mensagem Criptografada
        EncryptedMessage = cryptocode.encrypt(message, str(secretKey))

        # Enviando a mensagem pelo socket criado
        Socket_Client.send(EncryptedMessage.encode())
        
        Socket_Client.close()
        
        print("Conexão Finalizada!")
        break
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

        dir_path = 'C:/Users/Vitor/Desktop/projetoRedes/ProjetoRedes/Projeto 2 Servidor Web/Teste/Projeto2/servidor/'

        # list file and directories
        res = os.listdir(dir_path)

        if message1 in res:
            # Chave do cliente para arquivo
            with open('filekey.key', 'wb') as filekey:
                chaveArq = Socket_Client.recv(2048).decode()
                msg = cryptocode.decrypt(chaveArq, str(secretKey)).encode()
                filekey.write(msg)
            
            # Recebendo arquivo criptografado
            with open(message1, 'wb') as file:
                while 1:
                    # recebendo arquivo do servidor
                    data = Socket_Client.recv(2048)
                    if data == b'Arquivo solicitado entregue com sucesso!':
                        break
                    file.write(data)

            print(f'{message1} recebido!\n')

            # Abrindo a chave para descriptografar
            with open('filekey.key', 'rb') as filekey:
                key = filekey.read()

            # Usando a chave
            fernet = Fernet(key)

            # Abrindo o arquivo criptografado
            with open(message1, 'rb') as enc_file:
                encrypted = enc_file.read()

            # Descriptografando o arquivo
            decrypted = fernet.decrypt(encrypted)

            # Abrindo o arquivo no modo de gravação e gravando os dados descriptografados
            with open(message1, 'wb') as dec_file:
                dec_file.write(decrypted)
                
        else:
            print('Arquivo solicitado não existe.')

        print()

# fazer condicional para verificar se o cliente quer ocntinuar a conexao ou nao
# botar criptografia no arquivo e ver se fernet aguenta 4 clientes seguidos... ver solução q mandei pra thiago
# ver se o 2048 recebendo do cliente aguetna
