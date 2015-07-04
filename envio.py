from modulo import *

ModuloCom = ModuloCom()
ModuloCom.conf("configuracao.txt")
ModuloCom.start()


arquivos = open('/root/projeto/lista.txt','r+')
for linha in arquivos:
	ModuloCom.sendArquivo(linha)
