#!/usr/bin/env python2.7.12
#-*- coding: utf-8 -*-
import servidor

def modeloHTML(caminho):
	html = []
	html.append("<!DOCTYPE html>\n")
	html.append("<html>\n")
	html.append("<table>\n")
	html.append("<thead>\n")
	html.append("<tr>\n")
	html.append("<th>	Nome	</th>\n")
	html.append("<th>	Data de Modificação	</th>\n")
	html.append("<th>	Tamanho	</th>\n")
	html.append("</tr>\n")
	html.append("</thead>\n")
	html.append("<tbody>\n")
	html.append(visualizarArquivos(caminho))
	html.append("</tbody>\n")
	html.append("</table>\n")
	html.append("</html>\n")

	return ''.join(html)

'''def visualizarArquivos(caminho):

	arquivos = os.listdir(caminho)
	i=0
	info = []
	while(i<len(arquivos)):
		if(os.path.isdir(os.path.abspath(arquivos[i]))):
			#quer dizer que é um arquivo'''




