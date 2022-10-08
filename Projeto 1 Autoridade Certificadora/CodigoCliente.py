#Código do cliente usando TCP

import random
from socket import socket, AF_INET, SOCK_STREAM
import raizesPrimitivas


# Criando o socket
mClientSocket = socket(AF_INET, SOCK_STREAM)

# Colocando o socket para realizar solicitações
mClientSocket.connect(('localhost', 1235))

# # Criando chaves primas e a base ou seja as chaves "p" e "g"
# p = random.randint(0,999)
# while raizesPrimitivas.isPrime(p) == False:
#     p = random.randint(0,999)

# g = raizesPrimitivas.findPrimitive(p)

p = 23
g = 5

# Enviando as chaves padrões para o servidor
mClientSocket.send((f'{p} {g}').encode())

# Recebendo resposta do servidor
resp1 = mClientSocket.recv(2048).decode()
print(resp1)

valueA = random.randint(0, 999)
keyA = str((g ** valueA) % p)
mClientSocket.send(keyA.encode())

ChaveServidor = int(mClientSocket.recv(2048).decode())
print(f'A chave do servidor recebida foi {ChaveServidor}')

secretKey = (ChaveServidor ** valueA) % p
print(f'A chave compartilhada é {secretKey}')

mClientSocket.send(str(secretKey).encode())

resposta = mClientSocket.recv(2048)
sameKey = resposta.decode()

# Loop para o cliente enviar inúmeras solicitações/mensagens/arquivos

while True and (sameKey == str(secretKey)):
    message = input('Escreva a mensagem: ')

    # Enviando a mensagem pelo socket criado
    mClientSocket.send(message.encode())

    # Recebendo as respostas do servidor
    data = mClientSocket.recv(2048)
    
    # Decodificando a mensagem para mostrar a mensagem recebida
    reply = data.decode()
    print(f'Resposta recebida:{reply}')

