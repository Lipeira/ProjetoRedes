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
from email.utils import formatdate
from datetime import datetime
from time import mktime


# Função para mostrar os clientes conectados até o momento
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


# Função para limpar o console do terminal possibilitando uma melhor visualização
def LimparConsole():
    os.system("cls")


# Função para retornar mensagem de sucesso ao requisitar arquivo
def Success():
    now = datetime.now()
    mStamp = mktime(now.timetuple())

    # Cabeçalho das informações
    resposta = ''
    resposta += 'HTTP/1.1 200 OK\r\n'
    resposta += f'Date: {formatdate(timeval=mStamp, localtime=False, usegmt=True)}\r\n'
    resposta += 'Server: CIn UFPE/0.0.0.1 (Ubuntu)\r\n'
    resposta += 'Content-Type: text/html\r\n'

    print()
    # Mensagem do caso solicitado
    html = '\n'
    # html += '<html>'
    # html += '<head>'
    # html += '<title>Redes de Computadores - CIn/UFPE</title>'
    # html += '<meta charset="UTF-8">'
    # html += '</head>'
    # html += '<body>'
    # html += '<h1>Requisição bem sucedida, o objeto requisitado será enviado!</h1>'
    html += 'Requisição bem sucedida, o objeto requisitado será enviado!'
    # html += '</body>'
    # html += '</html>'

    resposta += html
    return resposta

# Função para retornar mensagem de arquivo não encontrado ao requisitar arquivo
def NotFound():
    now = datetime.now()
    mStamp = mktime(now.timetuple())

    # Cabeçalho das informações
    resposta = ''
    resposta += 'HTTP/1.1 404 Not Found\r\n'
    resposta += f'Date: {formatdate(timeval=mStamp, localtime=False, usegmt=True)}\r\n'
    resposta += 'Server: CIn UFPE/0.0.0.1 (Ubuntu)\r\n'
    resposta += 'Content-Type: text/html\r\n'

    print()
    # Mensagem do caso solicitado
    html = '\n'
    html += '<html>'
    html += '<head>'
    html += '<title>Not Found - CIn/UFPE</title>'
    html += '<meta charset="UTF-8">'
    html += '</head>'
    html += '<body>'
    html += '<h1>Essa requisição não foi encontrada no servidor!</h1>'
    html += '</body>'
    html += '</html>'

    resposta += html
    return resposta

# Função para retornar mensagem de erro de sintaxe ao requisitar arquivo
def BadRequest():
    now = datetime.now()
    mStamp = mktime(now.timetuple())
    
    # Cabeçalho das informações
    resposta = ''
    resposta += 'HTTP/1.1 400 Bad Request\r\n'
    resposta += f'Date: {formatdate(timeval=mStamp, localtime=False, usegmt=True)}\r\n'
    resposta += 'Server: CIn UFPE/0.0.0.1 (Ubuntu)\r\n'
    resposta += 'Content-Type: text/html\r\n'

    print()
    # Mensagm do caso solicitado
    html = '\n'
    html += '<html>'
    html += '<head>'
    html += '<title>Bad Request - CIn/UFPE</title>'
    html += '<meta charset="UTF-8">'
    html += '</head>'
    html += '<body>'
    html += '<h1>Mensagem de requisição não entendida pelo servidor, verifique se a mensagem de requisição está com algum erro de sintaxe!</h1>'
    html += '</body>'
    html += '</html>'

    resposta += html
    return resposta

# Função para retornar mensagem de acesso negado ao requisitar arquivo
def Forbidden():
    now = datetime.now()
    mStamp = mktime(now.timetuple())

    # Cabeçalho das informações
    resposta = ''
    resposta += 'HTTP/1.1 403 Forbidden\r\n'
    resposta += f'Date: {formatdate(timeval=mStamp, localtime=False, usegmt=True)}\r\n'
    resposta += 'Server: CIn UFPE/0.0.0.1 (Ubuntu)\r\n'
    # resposta += f'Content-Length: '
    resposta += 'Content-Type: text/html\r\n'

    print()
    # Mensagem do caso solicitado
    html = '\n'
    html += '<html>'
    html += '<head>'
    html += '<title>Forbidden - CIn/UFPE</title>'
    html += '<meta charset="UTF-8">'
    html += '</head>'
    html += '<body>'
    html += '<h1>Você não possui acesso a este conteúdo, logo, o servidor não pode aceitá-lo!</h1>'
    html += '</body>'
    html += '</html>'

    resposta += html
    return resposta

# Função para possibilitar a existência de threads (mais de um cliente) e possibilitar mais de uma requisição/resposta
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
    Socket_Client.send((cryptocode.encrypt(msgident, str(secretKey))).encode())

    ClientesConectados.append(CodCliente)
    LimparConsole()
    MostrarClientes()
    print(f'{branco}>> {verde}A chave secreta comum (compartilhada) é: {branco}{secretKey}')
    print(f"Novo Cliente Conectado: {CodCliente}")

    # Região do cliente para verificar se tem permissão ou não
    region1 = Socket_Client.recv(2048).decode()
    region = cryptocode.decrypt(region1, str(secretKey))

    # Geração da chave a ser usada pela biblioteca Fernet para criptografar arquivos
    key = Fernet.generate_key()

    # Salvando a chave em um arquivo para que o servidor sempre tenha conhecimento de como criptografar arquivos
    with open(str(CodCliente) + '.key', 'wb') as arq:
        arq.write(key)

    # Usando a chave gerada pela biblioteca Fernet
    fernetKey = Fernet(key)

    while IDclient[CodCliente] == sameKey:
        # Loop para o servidor receber diversas requisições de um mesmo cliente sem criar uma nova conexão

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
            ClientesConectados.remove(CodCliente)
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
                answer = Forbidden()
                print('Erro 403')
                rep403 = cryptocode.encrypt(answer, str(secretKey))
                Socket_Client.send(rep403.encode())
            
            else:
                # Fazendo a verificação da assinatura digital caso não dê forbidden
                try:
                    verification = rsa.verify(DecryptedMessage.encode(), newAssinatura, pubKey)
                    if verification == 'SHA-1':
                        print('A verificacao da requisicao concluida. Mensagem foi assinada/verificada.')


                    # Verificando o erro 400 de bad request
                    if "\\" in DecryptedMessage or "/" in DecryptedMessage or "*" in DecryptedMessage or "?" in DecryptedMessage or "<" in DecryptedMessage or ">" in DecryptedMessage or "|" in DecryptedMessage or "." not in DecryptedMessage or "'" in DecryptedMessage or '"' in DecryptedMessage:
                        answer = BadRequest()
                        print('Erro 400')
                        rep402 = cryptocode.encrypt(answer, str(secretKey))
                        Socket_Client.send(rep402.encode())

                    else:
                        # Pegando o path do arquivo no diretório
                        dir_path = str(pathlib.Path(__file__).parent.resolve()) + '/'
                        dir_path = dir_path.replace('\\', '/')
                        
                        # Lista contendo todos os diretórios e arquivos do path selecionado
                        res = os.listdir(dir_path)
                        
                        # Verificando se o arquivo solicitado se encontra na pasta para retornar 200 OK
                        if DecryptedMessage in res:
                            answer = Success()
                            print('200 OK')
                            rep200 = cryptocode.encrypt(answer, str(secretKey))
                            Socket_Client.send(rep200.encode())

                            # Abrindo o arquivo e pegando a chave que foi armazenado nele
                            with open(str(CodCliente) + '.key', 'rb') as arq:
                                chaveArquivo = arq.read().decode()
                            
                            # Verificando se a chave do arquivo é realmente igual a chave que foi gerada anteriormente
                            # Se for igual enviar ela para o cliente
                            if chaveArquivo == key.decode():
                                mensagem_Chave_Cliente = cryptocode.encrypt(chaveArquivo, str(secretKey))
                                Socket_Client.send(mensagem_Chave_Cliente.encode())
                                
                            # Se por algum motivo a chave não for igual mandar a que foi gerada primeiramente (original)
                            else:
                                chaveArquivo = key.decode()
                                mensagem_Chave_Cliente = cryptocode.encrypt(chaveArquivo, str(secretKey))
                                Socket_Client.send(mensagem_Chave_Cliente.encode())

                            # Abrindo o arquivo original para criptografar
                            with open(dir_path + DecryptedMessage, 'rb') as arquivo:
                                arquivoOriginal = arquivo.read()

                            # Criptografar o arquivo
                            fileCrypto = fernetKey.encrypt(arquivoOriginal)

                            # Abrindo o arquivo no modo de gravação e gravando os dados criptografados dentro do servidor (substituindo)
                            with open(dir_path + DecryptedMessage, 'wb') as fileEncrypt:
                                fileEncrypt.write(fileCrypto)

                            # Enviando arquivos criptografados direto para o cliente
                            with open(dir_path + DecryptedMessage, 'rb') as file:
                                for data in file.readlines():
                                    Socket_Client.send(data)

                                time.sleep(1)
                                rep = 'Arquivo solicitado entregue com sucesso!'
                                Socket_Client.send(rep.encode())

                            # Abrindo o arquivo criptografado que foi substituido dentro do servidor
                            with open(dir_path + DecryptedMessage, 'rb') as fileCry:
                                Encrypted = fileCry.read()

                            # Descriptografando o arquivo
                            fileDecrypto = fernetKey.decrypt(Encrypted)

                            # Abrindo o arquivo no modo de gravação e gravando os dados descriptografados dentro do servidor (substituindo)
                            with open(dir_path + DecryptedMessage, 'wb') as fileDecry:
                                fileDecry.write(fileDecrypto)

                        # Retornando Erro 404 de not found, pois arquivo não existe na pasta
                        else:
                            answer = NotFound()
                            print('Erro 404')
                            rep404 = cryptocode.encrypt(answer, str(secretKey))
                            Socket_Client.send(rep404.encode())

                # Se a mensagem se perder no caminho ou a assinatura digital/chave pública se corromperem irá dar 403 forbidden também
                except:
                    answer = Forbidden()
                    print('Erro 403')
                    rep403 = cryptocode.encrypt(answer, str(secretKey))
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
        conteudo, chave = linha.split()
        IDclient[conteudo] = chave

contador = 0

while True:
    # Loop para o servidor conseguir se conectar com vários clientes e colocando-o para aceitar as solicitações de conexão
    Socket_Client, clientAddr =  Socket_Server.accept()
    Thread(target=HandleRequest, args=(Socket_Client, clientAddr)).start()
