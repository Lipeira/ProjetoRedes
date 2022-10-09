#Código do cliente usando TCP

import random
from socket import socket, AF_INET, SOCK_STREAM
import raizesPrimitivas


# Criando o socket
Socket_Client = socket(AF_INET, SOCK_STREAM)

# Colocando o socket para realizar solicitações
Socket_Client.connect(('localhost', 54321))

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

valueA = random.randint(0, 999)
keyA = str((g ** valueA) % p)
Socket_Client.send(keyA.encode())

ChaveServidor = int(Socket_Client.recv(2048).decode())
# print(f'A chave do servidor recebida foi {ChaveServidor}')

secretKey = (ChaveServidor ** valueA) % p
print(f'A chave compartilhada: {secretKey}')

Socket_Client.send(str(secretKey).encode())

resposta = Socket_Client.recv(2048)
sameKey = resposta.decode()

# Loop para o cliente enviar inúmeras solicitações/mensagens/arquivos

while True:
    message = input('Escreva a mensagem: ')

    # Enviando a mensagem pelo socket criado
    Socket_Client.send(message.encode())

    # Recebendo as respostas do servidor
    data = Socket_Client.recv(2048)
    
    # Decodificando a mensagem para mostrar a mensagem recebida
    reply = data.decode()
    print(f'Resposta recebida:{reply}')

