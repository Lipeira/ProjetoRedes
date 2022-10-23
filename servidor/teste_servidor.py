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
import pathlib
import HtmlMessageIdeia

def MostrarClientes():
    vermelho = "\033[1;31m"
    verde = "\033[1;32m"
    vermelhobold = "\033[1;31;40m"
    branco = "\033[1;30m"
    azulclaro='\033[1;34m'
    print(f"{azulclaro}-- CLIENTES CONECTADOS --")
    counter = 1

    for client in ClientesConectados:        
        print(f"{azulclaro}- {verde}Cliente {counter}: {azulclaro}{client} -")
        counter += 1

    print("\n\n")

def LimparConsole():
    os.system("cls")

def HandleRequest(Socket_Client, mClientAddr):
    verde = "\033[1;32m"
    brancobold = "\033[1;30;40m"
    branco = "\033[1;30m"

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
    print(f'{branco}>> {verde}A chave compartilhada: {branco}{secretKey}')

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

    with escrita:
        escrita.write(f'{CodCliente} {sameKey} \n')

    msgident = f'>> Seu identificador é: {CodCliente}'
    Socket_Client.send(msgident.encode())

    ClientesConectados.append(CodCliente)
    LimparConsole()
    MostrarClientes()
    print(f"Novo Cliente Conectado: {CodCliente}")

    # Região do cliente para verificar se tem permissão ou não
    region = Socket_Client.recv(2048).decode()

    while IDclient[CodCliente] == sameKey:
        # Loop para O servidor receber diversas requisições de um mesmo cliente sem criar uma nova conexão
        # print('Esperando o próximo pacote ...')

        # Recebendo os dados do cliente e decodificando para mostrar o que foi recebido por ele
        # A mensagem recebida aqui está criptografada pelo cliente
        data = Socket_Client.recv(2048)

        LimparConsole()
        MostrarClientes()
        req = data.decode()
        print()
        print("--- Uma Mensagem foi Recebida ---")
        print(f'>> A mensagem criptografada foi: {req}')
        # Descriptografando a mensagem
        DecryptedMessage = cryptocode.decrypt(req, str(secretKey))

        # Verificação da Identificação do cliente com o segredo compartilhado
        ListDecrypted = DecryptedMessage.split("|")
        DecryptedMessage = ListDecrypted[0]
        sameKey = ListDecrypted[1]

        #Condição close connection

        if DecryptedMessage == "close":
            print(f"A conexão com o cliente {CodCliente} foi finalizada.")
            break

        else:
            print(f'>> Mensagem descriptografada: {DecryptedMessage}')
            print(f'>> Mensagem Recebida do cliente {CodCliente}')
            print()

            # Recebendo os dados enviados pelo cliente para verificar a assinatura digital
            dadosRSA = Socket_Client.recv(2048).decode()
            dados_RSA = dadosRSA.split('.....')

            # Recebendo assinatura do cliente 
            assinatura = dados_RSA[0]
            newAssinatura = bytes.fromhex(assinatura)

            # Dando um jeito de pegar a 1 chave da tupla da chave pública
            pubKey1 = dados_RSA[1]
            aux = pubKey1.split('(')
            values = aux[1]
            values_aux = values.split(',')
            a = values_aux[0]
            
            # Dando um jeito de pegar a 2 chave da tupla da chave pública
            aux2 = values_aux[1]
            aux3 = aux2.split()
            valueB = aux3[0]
            getB = valueB.split(')')
            b = getB[0]

            # Reinicializando a chave para voltar a classe PublicKey e realizar a verificação da assinatura digital
            pubKey = rsa.PublicKey(int(a), int(b))
            

            ############################################################
            # Projeto 2

            # Continuar aqui

            # Fazendo verificação do acesso aos arquivos, erro 403
            if region != '1':
                answer = HtmlMessageIdeia.Forbidden()
                print('Erro 403')
                rep403 = answer
                Socket_Client.send(rep403.encode())
            
            else:
                # Fazendo a verificação da assinatura digital caso não dê forbidden
                try:
                    verification = rsa.verify(DecryptedMessage.encode(), newAssinatura, pubKey)
                    if verification == 'SHA-1':
                        print('A verificacao da requisicao concluida. Mensagem foi assinada/verificada.')


                    # Verificando o erro 400 de bad request
                    if "\\" in DecryptedMessage or "/" in DecryptedMessage or "*" in DecryptedMessage or "?" in DecryptedMessage or "<" in DecryptedMessage or ">" in DecryptedMessage or "|" in DecryptedMessage or "." not in DecryptedMessage:
                        answer = HtmlMessageIdeia.BadRequest()
                        print('Erro 400')
                        rep402 = answer
                        Socket_Client.send(rep402.encode())

                    else:
                        # Pegando o path do arquivo no diretório
                        dir_path = str(pathlib.Path(__file__).parent.resolve()) + '/'
                        dir_path = dir_path.replace('\\', '/')
                        
                        # Lista contendo todos os diretórios e arquivos do path selecionado
                        res = os.listdir(dir_path)
                        
                        # Verificando se o arquivo solicitado se encontra na pasta para retornar 200 OK
                        if DecryptedMessage in res:
                            answer = HtmlMessageIdeia.sucesso()
                            print('200 OK')
                            rep200 = answer
                            Socket_Client.send(rep200.encode())

                            # geração de chave
                            key = Fernet.generate_key()

                            # Salvando chave em um arquivo
                            with open(str(CodCliente) + '.key', 'wb') as filekey:
                                filekey.write(key)

                            # Abrindo a chave para enviar para o cliente também
                            with open(str(CodCliente) + '.key', 'rb') as filekey:
                                key = filekey.read().decode()
                                msg = cryptocode.encrypt(key, str(secretKey))
                                Socket_Client.send(msg.encode())

                            # Usando a chave gerada
                            fernet = Fernet(key)

                            # Abrindo o arquivo original para criptografar
                            with open(dir_path + DecryptedMessage, 'rb') as file:
                                original = file.read()

                            # Criptografar o arquivo
                            encrypted = fernet.encrypt(original)

                            # Abrindo o arquivo no modo de gravação e gravando os dados criptografados
                            with open(dir_path + DecryptedMessage, 'wb') as encrypted_file:
                                encrypted_file.write(encrypted)

                            # Enviando arquivos para o cliente
                            with open(dir_path + DecryptedMessage, 'rb') as file:
                                for data in file.readlines():
                                    Socket_Client.send(data)

                                time.sleep(1)
                                rep = 'Arquivo solicitado entregue com sucesso!'
                                Socket_Client.send(rep.encode())

                            # Abrindo o arquivo criptografado
                            with open(dir_path + DecryptedMessage, 'rb') as enc_file:
                                encrypted = enc_file.read()

                            # Descriptografando o arquivo
                            decrypted = fernet.decrypt(encrypted)

                            # Abrindo o arquivo no modo de gravação e gravando os dados descriptografados
                            with open(dir_path + DecryptedMessage, 'wb') as dec_file:
                                dec_file.write(decrypted)

                        # Retornando Erro 404 de not found, pois arquivo não existe na pasta
                        else:
                            answer = HtmlMessageIdeia.NaoEncontrado()
                            print('Erro 404')
                            rep404 = answer
                            Socket_Client.send(rep404.encode())

                # Se a mensagem se perder no caminho ou a assinatura digital/chave pública se corromperem irá dar 403 forbidden também
                except:
                    answer = HtmlMessageIdeia.Forbidden()
                    print('Erro 403')
                    rep403 = answer
                    Socket_Client.send(rep403.encode())
                    print('A verificacao falhou. A mensagem nao pode ser verificada.')
            

LimparConsole()

#Cores Para Terminal Python

verde = "\033[1;32m"
branco = "\033[1;30m"
azulclaro='\033[1;34m'

# Criação do socket do servidor
Socket_Server = socket(AF_INET, SOCK_STREAM)
print(f'{branco}>> {azulclaro}Servidor criado...')

# Vinculando o socket do servidor a um endereço específico
Socket_Server.bind(('127.0.0.1', 13524))

# Colocando o servidor para escutar as solicitações de conexão dos inúmeros clientes
Socket_Server.listen()

IDclient = {}

ClientesConectados = []

leitura = open ('dicionario2.txt','r')

with leitura:
    for linha in leitura:
        chave, conteudo = linha.split()
        IDclient[chave] = conteudo

contador = 0

while True:
    # Loop para o servidor conseguir se conectar com vários clientes e colocando-o para aceitar as solicitações de conexão
    Socket_Client, clientAddr =  Socket_Server.accept()
    Thread(target=HandleRequest, args=(Socket_Client, clientAddr)).start()