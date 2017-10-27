#!/usr/bin/env python2.7.12
#-*- coding: utf-8 -*-
import socket
import unicodedata
import re
import sys

tamanhoBufferRecebimento = 4096

def tratamentoURL(url):
	url = url.split("http://")
	if(len(url)>1):
		url.pop(0)
	url = url[0]
	i=0
	while(url[i]!='/'):
		i=i+1
		if(i>=len(url)):break
	j=0
	nomeSite = []
	diretorioBuscado = []
	while(j<len(url)):
		if(j<i):
			nomeSite.append(url[j])
		else:
			diretorioBuscado.append(url[j])
		j=j+1
		if(j>=len(url)):break
	nomeSite = ''.join(nomeSite)
	diretorioBuscado = ''.join(diretorioBuscado)
	return nomeSite, diretorioBuscado

def analiseLexica(resposta):
	erros = [ "302 Found", "502 Bad Gateway", "404 Not Found", "301 Moved Permanently", "401 Unauthorized",  "400 Bad Request",  "403 Forbidden",  "500 Internal Server Error", "504 Gateway Timeout", "501 Not Implemented", "502 Bad Gateway", "503 Service Unavailable"]
	i=0
	while(i<len(erros)):
		if(re.search(erros[i], resposta)):
			return erros[i]
		i=i+1
	return False

def retiraCabecalho(resposta):
	i=0
	try:
		p = resposta.index('Content-Type:')
		while(1):
			if(resposta[p]=='\n'):
				p=p+1
				break
			i=0
			p=p+1
		i=0
		cabecalho = []
		while(i<p):
			cabecalho.append(resposta[i]) #cabecalho
			i=i+1
		cabecalho = ''.join(cabecalho)
		i=0
		rFinal = []
		p=p+1
		while(p<len(resposta)):
			rFinal.append(resposta[p])
			p=p+1
		return ''.join(rFinal)
	except:
		return resposta
	
def defineNome(diretorioBuscado):
	extensoes = ['.txt', '.mp3', '.pdf', '.html'] #adiciona extensões possíveis de serem impressas
	i=0
	diretorioBuscado = diretorioBuscado.split('/')
	while(i<len(extensoes)):
		if (diretorioBuscado[len(diretorioBuscado)-1].index(extensoes[i])):
			return diretorioBuscado[len(diretorioBuscado)-1]
		i=i+1
	return "arqGenerico"
def defineNomeSemDiretorio(url):
	try:
		p = url.index('www')
	except:
		p = None
	nome = []
	if(p==None):
		i=0
	else:
		i=5
	while(url[i]!='.'):
		nome.append(url[i])
		i=i+1
		if(i>=len(url)-1):break
	return ''.join(nome)+'.html'


def conectaServidor(url, porta, diretorioBuscado):

	ipSite	= socket.gethostbyname(url) #agora temos o ip do site
	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ipPorta = (url, int(porta))
	tcp.connect(ipPorta)
	if(len(diretorioBuscado)==0):
		tcp.send("GET / HTTP/1.1\nHost: "+url+"\nConnection: close\nUser-agent: Mozilla/5.0\n\n")
	else:
		tcp.send("GET "+diretorioBuscado+" HTTP/1.1\nHost: "+url+"\nConnection: close\nUser-agent: Mozilla/5.0\n\n")
	resposta = tcp.recv(tamanhoBufferRecebimento)
	erro = analiseLexica(resposta) #irá verificar se está tudo correto com o site
	if(erro == False): #não possui erro
		#vou salvar no arquivo
		resposta = retiraCabecalho(resposta)
		if(len(diretorioBuscado)!=0): #não estou buscando um diretório especifico
			nomeArq = defineNome(diretorioBuscado)
			arquivoSaida = open(nomeArq, 'w')
		else:
			nomeArq = defineNomeSemDiretorio(url)
			arquivoSaida = open(nomeArq, 'w')
		arquivoSaida.write(resposta)
	else: #possui erro
		print "\nO SITE REQUISITADO NÃO SERÁ SALVO DEVIDO AO ERRO '" + erro +"' TENTE OUTRO SITE, POR FAVOR !\n"
		exit()

opcao = sys.argv[1] # vai pegar a opção navegador ou servidor
url = sys.argv[2]
try:
	porta = sys.argv[3] #porta que será utilizada
except:
	porta = 80

if(opcao == "navegador"):
	url, diretorioBuscado = tratamentoURL(url)
	conectaServidor(url, porta, diretorioBuscado)
else:
	print "\nOPÇÃO PASSADA É INVÁLIDA !\n"
	exit()