#Código do Servidor

import random
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from typing import List
import cryptocode
import uuid
import rsa

def HandleRequest(Socket_Client, mClientAddr):
    # Recebendo chaves comuns "p" e "g" geradas pelo cliente
    dados = Socket_Client.recv(2048).decode()

    # Armazenando chaves separadas em duas variáveis sendo primo = "p" e raiz = "g"
    chaves = dados.split()
    primo = int(chaves[0])
    raiz = int(chaves[1])
    # print(f'O número primo recebido pelo cliente é {primo} e a raiz primitiva é {raiz}')

    # Confirmando o recebimento das chaves
    resposta = 'Chaves recebidas'
    Socket_Client.send(resposta.encode())

    # Gerando a chave do servidor (chave B) e enviando para o cliente
    valueB = random.randint(0,999)
    keyB = str((raiz ** valueB) % primo)
    Socket_Client.send(keyB.encode())


    # Recebendo chave do cliente (chave A)
    chaveCliente = int(Socket_Client.recv(2048).decode())   
    # print(f'A chave do cliente recebida foi {chaveCliente}')


    # Gerando chave compartilhada entre o servidor e o cliente
    secretKey = (chaveCliente ** valueB) % primo
    print(f'>> A chave compartilhada: {secretKey}')

    # Enviando chave para o cliente para que checar se é igual
    Socket_Client.send(str(secretKey).encode())

    # Recebendo chave compartilhada do cliente para confirmar se é igual
    respostaCliente = Socket_Client.recv(2048)
    sameKey = respostaCliente.decode()

    CodCliente = str(uuid.uuid4())
    while CodCliente in IDclient:
        CodCliente = str(uuid.uuid4())

    IDclient[CodCliente] = sameKey
    print(IDclient)

    msgident = f'>> Seu identificador é: {CodCliente}'
    Socket_Client.send(msgident.encode())

    while IDclient[CodCliente] == sameKey:
        # Loop para O servidor receber diversas requisições de um mesmo cliente sem criar uma nova conexão
        # print('Esperando o próximo pacote ...')

        # Recebendo os dados do cliente e decodificando para mostrar o que foi recebido por ele
        # A mensagem recebida aqui está criptografada pelo cliente
        data = Socket_Client.recv(2048)
        # print(f'>> A mensagem criptografada foi: {req}')
        req = data.decode()
        print("--- Uma Mensagem foi Recebida ---")
        print(f'>> A mensagem criptografada foi: {req}')
        # Descriptografando a mensagem
        DecryptedMessage = cryptocode.decrypt(req, str(secretKey))

        #Verificação da Identificação do cliente com o segredo compartilhado
        ListDecrypted = DecryptedMessage.split("|")
        DecryptedMessage = ListDecrypted[0]
        sameKey = ListDecrypted[1]
        print(f'>> Mensagem descriptografada: {DecryptedMessage}')
        print(f'>> Mensagem Recebida do cliente {CodCliente}')

        # Servidor mandando uma resposta para o cliente mostrando que o servidor está ativo e funcionando
        rep = '>> Mensagem enviada com sucesso...'
        Socket_Client.send(rep.encode())

# Criação do socket do servidor
Socket_Server = socket(AF_INET, SOCK_STREAM)
print('>> Servidor criado...')

# Vinculando o socket do servidor a um endereço específico
Socket_Server.bind(('127.0.0.1', 54321))

# Colocando o servidor para escutar as solicitações de conexão dos inúmeros clientes
Socket_Server.listen()

IDclient = {}
contador = 0

while True:
    # Loop para o servidor conseguir se conectar com vários clientes e colocando-o para aceitar as solicitações de conexão
    Socket_Client, clientAddr =  Socket_Server.accept()
    print(f'>> O servidor aceitou a conexao do cliente: {clientAddr}')
    
    Thread(target=HandleRequest, args=(Socket_Client, clientAddr)).start()