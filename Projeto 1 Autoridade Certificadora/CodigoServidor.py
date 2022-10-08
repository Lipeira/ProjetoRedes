#Código do Servidor

import random
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

def HandleRequest(mClientSocket, mClientAddr):
    dados = mClientSocket.recv(2048).decode()

    chaves = dados.split()
    primo = int(chaves[0])
    raiz = int(chaves[1])

    print(f'O número primo recebido pelo cliente é {primo} e a raiz primitiva é {raiz}')
    resposta = 'Chaves recebidas'
    mClientSocket.send(resposta.encode())

    valueB = random.randint(0,999)
    keyB = str((raiz ** valueB) % primo)
    mClientSocket.send(keyB.encode())

    chaveCliente = int(mClientSocket.recv(2048).decode())
    print(f'A chave do cliente recebida foi {chaveCliente}')

    secretKey = (chaveCliente ** valueB) % primo
    print(f'A chave compartilhada é {secretKey}')

    mClientSocket.send(str(secretKey).encode())

    respostaCliente = mClientSocket.recv(2048)
    sameKey = respostaCliente.decode()

    while True and (sameKey == str(secretKey)):
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


while True:
    # Loop para o servidor conseguir se conectar com vários clientes e colocando-o para aceitar as solicitações de conexão
    clientSocket, clientAddr =  mSocketServer.accept()
    print(f'O servidor aceitou a conexão do Cliente: {clientAddr}')
    
    Thread(target=HandleRequest, args=(clientSocket, clientAddr)).start()

