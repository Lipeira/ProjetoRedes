#Código do cliente usando TCP

import random
from socket import socket, AF_INET, SOCK_STREAM
import raizesPrimitivas2
import cryptocode
import rsa
import os
from cryptography.fernet import Fernet
import time

def LimparConsole():
    os.system("cls")

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
data = Socket_Client.recv(2048)
ident = data.decode()
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

Socket_Client.send(regiao.encode())

LimparConsole()

# Loop para o cliente enviar inúmeras solicitações/mensagens/arquivos
while True:
    print()
    # Mensagem que o cliente deseja enviar
    print('''Escolha um dos arquivos para receber: 
    [1] Paris.jpg 
    [2] postagem.png
    [3] teste.pdf

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
        codeSplit = code.split()

        # Se o código for 200 irá receber o arquivo criptografado e descriptografar para a visualização
        if codeSplit[1] == '200':

            print(code)

            # Chave do cliente para arquivo
            with open(str(identify) + '.key', 'wb') as filekey:
                chaveArq = Socket_Client.recv(2048).decode()
                msg = cryptocode.decrypt(chaveArq, str(secretKey)).encode()
                filekey.write(msg)
            
            # Recebendo arquivo criptografado
            with open(message1, 'wb') as file:
                while 1:
                    # recebendo arquivo do servidor
                    data = Socket_Client.recv(1000000)
                    if data == b'Arquivo solicitado entregue com sucesso!':
                        break
                    file.write(data)

            print(f'{message1} recebido!\n')

            # Abrindo a chave para descriptografar
            with open(str(identify) + '.key', 'rb') as filekey:
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
        
        # Caso não retorne o código 200 irá gerar os erros específicos
        elif codeSplit[1] == '403':
            print(code)

        elif codeSplit[1] == '404':
           print(code)

        else:
            print(code)



# COMENTÁRIOS PARA MELHORAR CÓDIGO


# fazer condicional para verificar se o cliente quer ocntinuar a conexao ou nao
# botar criptografia no arquivo e ver se fernet aguenta 4 clientes seguidos... ver solução q mandei pra thiago
# tem problema do fernet --> 1 cliente solicitar algo e o 1 morrer...............
# ver se o 2048 recebendo do cliente aguetna 

# 1 - feito
# 2 e 3- salvar cada arquivo com o cod do cliente para criar varios arqs...
# 4 - aguenta!!!

# OBS: assinatura as vezes funciona e as vezes nao (na maioria funciona... talvez o numero das chaves nao seja fixo???)
# o get é só a pergunta??
# o servidor web é só enviar arquivo??
# questões sobre o forbidden...
# mensagem em cada caso só copiar aquela msg?
# COMO botar caminho diretório generico 

# 1 - olhar com calma depois...
# 2 - sim. o input é o get ---> criar um if para fazer ter 3 opções de escolha
# 3 -  sim ---> testar com arquivos grandes dps (50Mb)
# 4 - fazer algum jeito de analisar o identificador do cliente... para corromper e garantir que nao tenha permissao (verification failed do verify do RSA)
# 5 - sim, só dar import no html message dela e usar para printar
# 6 - pathfile lab para deixar um path genérico independente de quem acessar!! -> falar com thiago depois,.....
# ---> pathlib absolute() swap \\ para /