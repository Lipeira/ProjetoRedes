import socket
import os

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(('localhost', 7777))
print('Conectado!!')


while True:
    nameDirectory = str(input('Diretorio>'))

    namefile = str(input('Arquivo>'))

    dir_path = nameDirectory

    # list file and directories
    res = os.listdir(dir_path)

    client.send((f'{nameDirectory} {namefile}').encode())

    if namefile in res:
        with open(namefile, 'wb') as file:
            while 1:
                data = client.recv(1500000000)
                if not data:
                    break
                file.write(data)

            print(f'{namefile} recebido!')
            
    else:
        resp = client.recv(2048).decode()
        print(resp)

# 1500000000
# pergunta 1) nao consegue fazer troca de arquivos simultâneos
# pergunta 2) como conectar o GET
# pergunta 3) diferença entre webServer e httpServer
# pergunta 4) SOBRE PROJETO 1 -> sobre certificado / assinatura digital... (cliente consegue assinar mas servidor verifica dá erro)
# pergunta 5) pq no webServer retorna uma mensagem de HTTP OK 200 fixos?
# pergunta 6) diferença entre notfound e badRequest (seria ; . , - ^ ?)
# pergunta 7) como fazer o forbidden??

# RESPOSTAS:

# 1 - verificar conexão (o servidor esta´morrendo... falta while no servidor pra atender varios...)
# 2 -> o GET é do cliente pro servidor pra pegar os arquivos? conectar com cabeçalho? fazer tudo? botar criptografia/assinatura no payload? verificação..... etc etc etc bla bla
# 3 -> httpServer foi só p mostrar algo NÃO USAR!!!! só WEBSERVER
# 4 -> ela vai ver e até de noite responde!!!
# 5 -> foi só um exemplo... mas se for retornar 200 ok tem q seguir aquele padrao
# 6 -> bad request é algo que o servidor não entende... pode ser algo escrito errado
# 7 -> o forbidden pode ser feito corrompendo a chave (mudando) para bloquear o acesso

