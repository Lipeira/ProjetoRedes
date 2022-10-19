from socket import socket, AF_INET, SOCK_STREAM
import HtmlMessageIdeia

def VerifyGet(msg):
    msglist = msg.split()
    archive = msglist
    cond = True
    if cond:
        #Verificar se o arquivo existe
        return "notfound"
    elif cond:
        #Verificar se a mensagem foi corrompida
        return "badrequest"
    elif cond:
        #Verificar se o cliente tem permissão
        return "forbidden"
    else:
        return "ok"

#1)Criar o socket servidor:
webServerSocket = socket(AF_INET, SOCK_STREAM)
webServerSocket.bind(('localhost', 9696))
webServerSocket.listen()

#2)Aceitar as solicitações dos clientes:
while True:
    print('Esperando Solicitações ....')
    clientSocket, clientAddress = webServerSocket.accept()
    #Recebendo dados do cliente
    data = clientSocket.recv(2048)


    #Respondendo a solicitação
    #Verificar qual mensagem mandar para o cliente como resposta
    response = VerifyGet(data)

    if response == 'ok':
        msgresponse = HtmlMessageIdeia.sucesso()
    elif response == 'notfound':
        msgresponse = HtmlMessageIdeia.NaoEncontrado()
    elif response == 'forbidden':
        msgresponse = HtmlMessageIdeia.Forbidden()
    elif response == 'badrequest':
        msgresponse = HtmlMessageIdeia.BadRequest()

    clientSocket.send(msgresponse.encode())

#clientSocket.close()
#webServerSocket.close()