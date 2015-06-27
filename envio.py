from modulo import *

ModuloCom = ModuloCom()
ModuloCom.conf("configuracao.txt")


arquivos = open('/root/projeto/listadentro.txt','r+')
for linha in arquivos:
	ModuloCom.sendArquivo(linha)
	
ModuloCom.start()

