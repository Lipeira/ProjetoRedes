import socket
import glob, os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(('localhost', 7777))
server.listen(1)

connection, address = server.accept()

names = connection.recv(1024).decode()
Names = names.split()
diretorio = Names[0]
namefile = str(Names[1])

#######################

directory = "novaPasta"
	
parent_dir = "C:/Users/Vitor/Desktop/projetoRedes/projetoRedes"
	
path = os.path.join(parent_dir, directory)

#########################


dir_path = 'C:/Users/Vitor/Desktop/Socket/Servidor/'
# list file and directories
res = os.listdir(dir_path)

print(res)
print()
#########################

try: 
    if namefile in res:

        with open(diretorio + namefile, 'rb') as file:
            for data in file.readlines():
                connection.send(data)

            print('Arquivo enviado')
        
    else:
        rep = 'O arquivo solicitado não existe'
        connection.send(rep.encode())

        print('Arquivo não encontrado!')

except:
    os.mkdir(path)
    print(f'A pasta nao existe. Nova pasta criada: {directory}')

# C:/Users/Vitor/Desktop/Socket/novaPasta/
# C:/Users/Vitor/Desktop/Socket/Servidor/

# C:/Users/Vitor/Desktop/projetoRedes/ProjetoRedes/teste_Servidor/
# C:\Users\Vitor\Desktop\projetoRedes\ProjetoRedes\teste_Servidor\Paris.jpg
