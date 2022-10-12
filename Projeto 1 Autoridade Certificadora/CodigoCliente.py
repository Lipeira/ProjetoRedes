#Código do cliente usando TCP

import random
from socket import socket, AF_INET, SOCK_STREAM
import raizesPrimitivas
import cryptocode
import rsa

# Criando o socket
Socket_Client = socket(AF_INET, SOCK_STREAM)

# Colocando o socket para realizar solicitações
Socket_Client.connect(('localhost', 54321))

(pubKey, privKey) = rsa.newkeys(512)

# Criando chaves primas e a base ou seja as chaves "p" e "g"
p = random.randint(0, 999)
while raizesPrimitivas.isPrime(p) == False:
    p = random.randint(0, 999)

g = raizesPrimitivas.findPrimitive(p)


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
    message = input('>> Escreva a mensagem: ')
    message = message + f"|{sameKey}"

    # Mensagem Criptografada
    EncryptedMessage = cryptocode.encrypt(message, str(secretKey))

    # Enviando a mensagem pelo socket criado
    Socket_Client.send(EncryptedMessage.encode())

    # Fazendo assinatura digital e enviando dados para o servidor verificar
    sign = rsa.sign(message.encode(), privKey, 'SHA-1')

    # print(sign)

    # verification = rsa.verify(message.encode(), sign, pubKey)

    # print(verification) -----> pq funciona no cliente e no servidor não???

    Socket_Client.send((f'{sign}.....{pubKey}').encode())


    # Recebendo as respostas do servidor
    data = Socket_Client.recv(2048)
    
    # Decodificando a mensagem para mostrar a mensagem recebida
    reply = data.decode()
    print(f'>> {reply}')
    print()

