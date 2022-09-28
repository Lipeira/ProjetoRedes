#Código do cliente usando TCP

import random
from socket import socket, AF_INET, SOCK_STREAM

# Criando o socket
mClientSocket = socket(AF_INET, SOCK_STREAM)

# Colocando o socket para realizar solicitações
mClientSocket.connect(('localhost', 1235))


# Recebendo chave gerada pelo servidor
data = mClientSocket.recv(2048)
Chave = data.decode()
print(f"Sua chave privada é de: {Chave}")


# Loop para o cliente enviar inúmeras solicitações/mensagens/arquivos

while True:
    message = input('Escreva a mensagem: ')

    # Enviando a mensagem pelo socket criado
    mClientSocket.send(message.encode())

    # Recebendo as respostas do servidor
    data = mClientSocket.recv(2048)
    
    # Decodificando a mensagem para mostrar a mensagem recebida
    reply = data.decode()
    print(f'Resposta recebida:{reply}')

