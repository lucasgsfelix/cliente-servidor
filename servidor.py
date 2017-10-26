#!/usr/bin/env python2.7.12
#-*- coding: utf-8 -*-
import socket
import unicodedata
import re
import sys
import os
import mimetypes

#ipServidor = '192.168.54.17'
ipServidor = '172.18.2.218'
tamanhoBufferEnvio = 5124
tamanhoBufferRecebimento = 1024
def trataArquivo(caminho):
	try:
		arqSaida = open(caminho, "r")
		arqSaida = arqSaida.read()
		return arqSaida
	except:
		return caminho

def interpretaMensagem(mensagemCliente):
	mensagemCliente = mensagemCliente.split('\n')
	if(mensagemCliente[0] == "GET / HTTP/1.1\r"): #envio todos os arquivos que estão no caminho, só dando uma olhada
		return os.listdir(caminho), None
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
			if(caminho[len(caminho)-1]=='/'):
				file = caminho + arquivoRequisitado
			else:
				file = caminho + '/' + arquivoRequisitado
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
	elif(type(resposta)==list):
		con.send("HTTP/1.1 200 OK\nContent-Type: Text\n\n")
		i=0
		con.send("\nOs arquivos disponíveis são: \n")
		while(i<len(resposta)):
			con.send(resposta[i]) #envio agora o arquivo
			resposta[i].flush()
			i=i+1
	else:
		con.send(resposta)
		resposta.flush()

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

	caminho = sys.argv[1]
	try:
		porta = sys.argv[2] #porta que será utilizada
	except:
		porta = 8080
	conecta(porta, caminho)