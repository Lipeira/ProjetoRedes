#Código do cliente

#Código TCP
import random
from socket import socket, AF_INET, SOCK_STREAM

# Criando o socket
mClientSocket = socket(AF_INET, SOCK_STREAM)

# Colocando o socket para realizar solicitações
mClientSocket.connect(('localhost', 1235))

data = mClientSocket.recv(2048)
ChavePrivada = data.decode()
print(f"Sua chave privada é de: {ChavePrivada}")

while True:
    # Este loop foi criado apenas para que o cliente conseguisse enviar múltiplas solicitações
    message = input('>>')
    #Enviando a mensagem pelo socket criado.
    mClientSocket.send(message.encode())
    #Recebendo as respostas do servidor.
    data = mClientSocket.recv(2048)
    reply = data.decode()
    print(f'Resposta recebida:{reply}')

