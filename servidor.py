#!/usr/bin/env python2.7.12
#-*- coding: utf-8 -*-
import socket
import unicodedata
import re
import sys
import os
import mimetypes
import defineHTML

ipServidor = '192.168.54.17'
#ipServidor = '172.18.2.218'
tamanhoBufferEnvio = 5124
tamanhoBufferRecebimento = 1024
def trataArquivo(caminho):
	try:
		arqSaida = open(caminho, "r")
		arqSaida = arqSaida.read()
		return arqSaida
	except:
		return caminho

def interpretaMensagem(mensagemCliente, caminho):
	mensagemCliente = mensagemCliente.split('\n')
	if(mensagemCliente[0] == "GET / HTTP/1.1\r"): #envio todos os arquivos que estão no caminho, só dando uma olhada
		try:
			return os.listdir(caminho), None
		except:
			print "\nCaminho específicado pelo usuário é inexistente!\n"
			return "HTTP/1.1 404 NOT FOUND", None
	else: #tá querendo um arquivo
		msg = mensagemCliente[0]
		arquivoRequisitado = []
		i=4
		extensao = []
		while(msg[i]!=' '):
			arquivoRequisitado.append(msg[i])
			i=i+1
		arquivoRequisitado = ''.join(arquivoRequisitado)
		extensao = avaliaExtensao(arquivoRequisitado)
		if(arquivoRequisitado!="/favicon.ico"):
			file = caminho + arquivoRequisitado
			
		else:
			file = caminho
		v = os.path.exists(file)

		if(v==True): #envio o arquivo que foi requisitado
			return trataArquivo(file), extensao[0]
		else:
			print "\n\nO ARQUIVO REQUISITADO PELO USUÁRIO NÃO ESTÁ DISPONÍVEL!\n\n"
			return "HTTP/1.1 404 NOT FOUND", None

def avaliaExtensao(resposta):
	list(resposta).remove('/')
	resposta = ''.join(resposta)
	return mimetypes.guess_type(resposta, strict= True)


def enviaMensagem(resposta, con, extensao):
	
	if(resposta!="HTTP/1.1 404 NOT FOUND") and (extensao!=None): 
		con.send("HTTP/1.1 200 OK\nContent-Type: "+extensao+"\n\n")	
		con.send(resposta)
		con.close()	
	
	elif(type(resposta)==list):
		con.send("HTTP/1.1 200 OK\nContent-Type: Text\n\n")
		i=0
		con.send("Os arquivos disponíveis são: \n")
		while(i<len(resposta)):
			resposta[i] = resposta[i] + '\n'
			i=i+1
		
		con.send(''.join(resposta)) #envio agora o arquivo
		con.close()
	else:
		con.send(resposta)
		con.close()

def conecta(porta, caminho):

	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ipPorta = (ipServidor, int(porta))
	tcp.bind(ipPorta)
	tcp.listen(5) #ouve as conexões feitas no socket, parametro é o número máximo de conexões permitidas
	print "SERVIDOR INICIADO..."
	while (1):
		con, cliente = tcp.accept() #irá aceitar os clientes que tentarem se conectar
		processoX = os.fork() #irá dividir entre as threads os processos
		if (processoX == 0): #quer dizer há mais cliente
			print "CONECTADO PELO CLIENTE", cliente
			while (1):
				mensagemCliente = con.recv(tamanhoBufferRecebimento)
				resposta, extensao = interpretaMensagem(mensagemCliente, caminho)
				enviaMensagem(resposta, con, extensao)
				#analisar para mandar a mensagem de volta
				if not mensagemCliente: break
			con.close() #fecho cliente
		else:
			con.close()

if __name__ == "__main__":
	try:
		caminho = sys.argv[1]
	except:
		print "VOCÊ PRECISA ESPECIFICAR UM CAMINHO PARA QUE O MESMO SEJA ACESSADO ! \n"
		exit()
	try:
		porta = sys.argv[2] #porta que será utilizada
	except:
		porta = 8080
	if(caminho[len(caminho)-1]!='/'):
		caminho = caminho + '/'
	conecta(porta, caminho)