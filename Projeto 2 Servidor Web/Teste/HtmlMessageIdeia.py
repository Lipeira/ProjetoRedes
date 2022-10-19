from email.utils import formatdate
from datetime import datetime
from time import mktime

def sucesso(ContentType,Archive):
    now = datetime.now()
    mStamp = mktime(now.timetuple())

    #header
    resposta = ''
    resposta += 'HTTP/1.1 200 OK\r\n'
    resposta += f'Date: {formatdate(timeval=mStamp, localtime=False, usegmt=True)}\r\n'
    resposta += 'Server: CIn UFPE/0.0.0.1 (Ubuntu)\r\n'
    # resposta += f'Content-Length: '
    resposta += 'Content-Type: text/html\r\n'
    resposta += '\r\n'

    #mensagem
    html = ''
    html += '<html>'
    html += '<head>'
    html += '<title>Redes de Computadores - CIn/UFPE</title>'
    html += '<meta charset="UTF-8">'
    html += '</head>'
    html += '<body>'
    html += '<h1>Requisição bem sucedida, o objeto requisitado será enviado!</h1>'
    html += '</body>'
    html += '</html>'

    resposta += html
    return resposta

def NaoEncontrado(ContentType,Archive):
    now = datetime.now()
    mStamp = mktime(now.timetuple())

    resposta = ''
    resposta += 'HTTP/1.1 404 Not Found\r\n'
    resposta += f'Date: {formatdate(timeval=mStamp, localtime=False, usegmt=True)}\r\n'
    resposta += 'Server: CIn UFPE/0.0.0.1 (Ubuntu)\r\n'
    # resposta += f'Content-Length: '
    resposta += 'Content-Type: text/html\r\n'
    resposta += '\r\n'

    html = ''
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

def BadRequest(ContentType,Archive):
    now = datetime.now()
    mStamp = mktime(now.timetuple())

    resposta = ''
    resposta += 'HTTP/1.1 400 Bad Request\r\n'
    resposta += f'Date: {formatdate(timeval=mStamp, localtime=False, usegmt=True)}\r\n'
    resposta += 'Server: CIn UFPE/0.0.0.1 (Ubuntu)\r\n'
    # resposta += f'Content-Length: '
    resposta += 'Content-Type: text/html\r\n'
    resposta += '\r\n'

    html = ''
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

def Forbidden(ContentType,Archive):
    now = datetime.now()
    mStamp = mktime(now.timetuple())

    resposta = ''
    resposta += 'HTTP/1.1 403 Forbidden\r\n'
    resposta += f'Date: {formatdate(timeval=mStamp, localtime=False, usegmt=True)}\r\n'
    resposta += 'Server: CIn UFPE/0.0.0.1 (Ubuntu)\r\n'
    # resposta += f'Content-Length: '
    resposta += 'Content-Type: text/html\r\n'
    resposta += '\r\n'

    html = ''
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

#Implementação GET para o cliente
#Archive: paris.jpg, carro.txt
def Get(Archive):

    #header
    msg = ''
    msg += f'GET /{Archive} HTTP/1.1\r\n'
    msg += f'Host: localhost\r\n'
    msg += 'Connection: keep-alive\r\n'
    msg += 'Accept-Language: pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7\r\n'
    msg += '\r\n'
    
    return msg


def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write(self.path.encode())


# from http.server import HTTPServer, BaseHTTPRequestHandler

# class handleRequest(BaseHTTPRequestHandler):
#     def do_GET(self):
#         self.send_response(200)
#         self.send_header('content-type', 'text/html')
#         self.end_headers()
#         self.wfile.write(self.path.encode())

# httpServer = HTTPServer(('localhost',9090), handleRequest)
# print('O servidor está ativo!')
# httpServer.serve_forever()
