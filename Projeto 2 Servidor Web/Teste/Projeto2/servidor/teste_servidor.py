#Código do Servidor

import random
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from typing import List
import cryptocode
import uuid
import rsa
import os
from cryptography.fernet import Fernet
import time
import HtmlMessageIdeia

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


    escrita = open ('dicionario2.txt','a')

    IDclient[CodCliente] = sameKey
    print(IDclient)

    with escrita:
        escrita.write(f'{CodCliente} {sameKey} \n')

    msgident = f'>> Seu identificador é: {CodCliente}'
    Socket_Client.send(msgident.encode())

    while IDclient[CodCliente] == sameKey:
        # Loop para O servidor receber diversas requisições de um mesmo cliente sem criar uma nova conexão
        # print('Esperando o próximo pacote ...')

        # Recebendo os dados do cliente e decodificando para mostrar o que foi recebido por ele
        # A mensagem recebida aqui está criptografada pelo cliente
        data = Socket_Client.recv(2048)

        req = data.decode()
        print("--- Uma Mensagem foi Recebida ---")
        print(f'>> A mensagem criptografada foi: {req}')
        # Descriptografando a mensagem
        DecryptedMessage = cryptocode.decrypt(req, str(secretKey))

        # Verificação da Identificação do cliente com o segredo compartilhado
        ListDecrypted = DecryptedMessage.split("|")
        DecryptedMessage = ListDecrypted[0]
        sameKey = ListDecrypted[1]
        print(f'>> Mensagem descriptografada: {DecryptedMessage}')
        print(f'>> Mensagem Recebida do cliente {CodCliente}')
        print()

        # Recebendo os dados enviados pelo cliente para verificar a assinatura digital
        dadosRSA = Socket_Client.recv(2048).decode()
        dados_RSA = dadosRSA.split('.....')

        assinatura = dados_RSA[0]
        newAssinatura = bytes.fromhex(assinatura)
        pubKey1 = dados_RSA[1]
        a = pubKey1[10:164]

        b = pubKey1.split(' ')
        aux = b[1]
        aux1 = aux[0:-1]
            
        pubKey = rsa.PublicKey(int(a), int(aux1))

        try:
            verification = rsa.verify(DecryptedMessage.encode(), newAssinatura, pubKey)
            if verification == 'SHA-1':
                print('A verificacao da requisicao concluida. Mensagem considerada autentica e foi assinada/verificada.')

        except:
            print('A verificacao falhou. A mensagem nao e autentica e nao pode ser verificada.')
        

        ############################################################
        # Projeto 2
        
        # Continuar aqui

        # geração de chave
        key = Fernet.generate_key()

        # string a chave em um arquivo
        with open('filekey.key', 'wb') as filekey:
            filekey.write(key)

        # abrindo a chave
        with open('filekey.key', 'rb') as filekey:
            key = filekey.read()
            dado = key.decode()
            msgCriptografada = cryptocode.encrypt(dado, str(secretKey))
            Socket_Client.send(msgCriptografada.encode())

        # usando a chave gerada
        fernet = Fernet(key)

        dir_path = 'C:/Users/Vitor/Desktop/Teste2/Teste/Projeto2/servidor/'

        # list file and directories
        res = os.listdir(dir_path)


        # abrindo o arquivo original para criptografar
        with open(dir_path + DecryptedMessage, 'rb') as file:
            original = file.read()

        # criptografar o arquivo
        encrypted = fernet.encrypt(original)

        # abrir o arquivo no modo de gravação e
        # gravar os dados criptografados
        with open(dir_path + DecryptedMessage, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)


        if DecryptedMessage in res:
            with open(dir_path + DecryptedMessage, 'rb') as file:
                for data in file.readlines():
                    Socket_Client.send(data)

                time.sleep(1)
                rep = 'Arquivo solicitado entregue com sucesso!'
                Socket_Client.send(rep.encode())

            # abrindo o arquivo criptografado
            with open(dir_path + DecryptedMessage, 'rb') as enc_file:
                encrypted = enc_file.read()

            # descriptografando o arquivo
            decrypted = fernet.decrypt(encrypted)

            # abrindo o arquivo no modo de gravação e
            # gravando os dados descriptografados
            with open(dir_path + DecryptedMessage, 'wb') as dec_file:
                dec_file.write(decrypted)

        else:
            print('O arquivo nao foi encontrado!')


# Criação do socket do servidor
Socket_Server = socket(AF_INET, SOCK_STREAM)
print('>> Servidor criado...')

# Vinculando o socket do servidor a um endereço específico
Socket_Server.bind(('127.0.0.1', 13524))

# Colocando o servidor para escutar as solicitações de conexão dos inúmeros clientes
Socket_Server.listen()

IDclient = {}


leitura = open ('dicionario2.txt','r')

with leitura:
    for linha in leitura:
        chave, conteudo = linha.split()
        IDclient[chave] = conteudo

contador = 0

while True:
    # Loop para o servidor conseguir se conectar com vários clientes e colocando-o para aceitar as solicitações de conexão
    Socket_Client, clientAddr =  Socket_Server.accept()
    print(f'>> O servidor aceitou a conexao do cliente: {clientAddr}')
    
    Thread(target=HandleRequest, args=(Socket_Client, clientAddr)).start()
