#Código do Servidor

import random
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


# Função diffie hellman para gerar chaves criptografadas para cada cliente 
# O Diffie Hellman gera chaves assimétricas então temos uma chave pública e privada

def diffie_hellman():
    A = random.randint(1,999999)
    B = random.randint(1,999999)
    X = random.randint(1,999999)
    Y = random.randint(1,999999)

    Ra = (Y**A) % X
    Rb = (Y**B) % X

    KeyA = (Rb**A) % X
    KeyB = (Ra**B) % X

    if KeyA == KeyB:
        return KeyA

def HandleRequest(mClientSocket, mClientAddr):
    while True:
        # Loop para O servidor receber diversas requisições de um mesmo cliente sem criar uma nova conexão
        print('Esperando o próximo pacote ...')

        # Recebendo os dados do cliente e decodificando para mostrar o que foi recebido por ele
        data = mClientSocket.recv(2048)
        print(f'Requisição recebida de {mClientAddr}')
        req = data.decode()
        print(f'A requisição foi:{req}')

        # Servidor mandando uma resposta para o cliente mostrando que o servidor está ativo e funcionando
        rep = 'Hey cliente!'
        mClientSocket.send(rep.encode())

# Criação do socket do servidor

mSocketServer = socket(AF_INET, SOCK_STREAM)
print(f'Socket criado ...')

# Vinculando o socket do servidor a um endereço específico
mSocketServer.bind(('127.0.0.1',1235))

# Colocando o servidor para escutar as solicitações de conexão dos inúmeros clientes
mSocketServer.listen()

dic = {}

while True:
    # Loop para o servidor conseguir se conectar com vários clientes e colocando-o para aceitar as solicitações de conexão
    clientSocket, clientAddr =  mSocketServer.accept()
    print(f'O servidor aceitou a conexão do Cliente: {clientAddr}')
    
    # Definindo as chaves privadas de cada cliente e criando múltiplas threads para que o servidor consiga responder mais de um cliente por vez.
    ChaveGerada = diffie_hellman()
    msgcripto = f"{ChaveGerada}"
    clientSocket.send(msgcripto.encode())

    dic[ChaveGerada] = clientAddr
    Thread(target=HandleRequest, args=(clientSocket, clientAddr)).start()

