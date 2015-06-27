import netinfo
import smtplib
import mimetypes
import ftplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import socket
import requests
import httplib
import urllib
import time
import ConfigParser
import threading

timeout = 25
socket.setdefaulttimeout(timeout)

class ModuloCom(threading.Thread):


	def conf(self,arquivoConfi):
		config = ConfigParser.ConfigParser()
		config.read(arquivoConfi)
		self.checkDestino = config.get("configuracao", "Destino")
		self.interfaceETH0 = config.get("configuracao", "interfaceETH0")
                self.interfacePPP0 = config.get("configuracao", "interfacePPP0")
                self.fromEmail = config.get("configuracao", "fromEmail")
                self.toEmail = config.get("configuracao", "toEmail")
                self.usuarioEmail = config.get("configuracao", "usuarioEmail")
                self.senhaEmail = config.get("configuracao", "senhaEmail")
                self.nomeArquivoEmail = config.get("configuracao", "nomeArquivoEmail")
                self.servidoFtp = config.get("configuracao", "servidoFtp")
                self.loginFtp = config.get("configuracao", "loginFtp")
                self.senhaFtp = config.get("configuracao", "senhaFtp")
                self.nomeArquivoFtp = config.get("configuracao", "nomeArquivoFtp")
                self.nomeArquivoHttp = config.get("configuracao", "nomeArquivoHttp")

	
	def sendArquivo(self,arquivoEnviado):
                arquivosmtp = open(self.nomeArquivoEmail, "r+")
                arquivoftp = open(self.nomeArquivoFtp, "r+")
                arquivohttp = open(self.nomeArquivoHttp, "r+")
                oldsmtp = arquivosmtp.read()
                oldftp = arquivoftp.read()
                oldhttp = arquivohttp.read()
                arquivosmtp.seek(0)
                arquivoftp.seek(0)
                arquivohttp.seek(0)
                arquivosmtp.write(str(arquivoEnviado + oldsmtp ))
                arquivoftp.write(str(arquivoEnviado + oldftp ))
                arquivohttp.write(str(arquivoEnviado + '\n' + oldhttp ))
                arquivosmtp.close()
                arquivoftp.close()
                arquivohttp.close()


	def gerenciaEnvio(self):
		while 1:
                        if self.verificaInterface() == False:
                                print "Nao existe Interface  Disponivel"
                                break
                        if self.checkStatus() == False:
                                print "Sem rota para Internet"

                        self.sendEnvio()
                        break

	def run(self):
                self.gerenciaEnvio()

	
	def sendEnvio(self):
		self.conexaoEmail()
                self.conexaoFtp()
		
	
	def checkStatus(self):
                primeiroEth0 = os.system("ping -I eth0  -c 5 " + self.checkDestino )
                segundaPpp0 = os.system("ping -I ppp0  -c 5 " + self.checkDestino )
		if primeiroEth0 == 0 or segundaPpp0  == 0:
                        print "Conexao OK"
                        return True
                else:
                        print "Conexao OFF"
                        return False


        def verificaInterface(self):
                        for dev in netinfo.list_active_devs():
                                 print dev
			if self.interfaceETH0 == dev:
                        	print "Interface eth0 OK"
                                return True

                        if self.interfacePPP0 == dev:
                                print "Interface ppp0 OK"
                                return True

                        else:
                                print "Sem interface"
                                return False


        def conexaoEmail(self):
                try:
                        emailfrom = self.fromEmail
                        emailto = self.toEmail
                        user = self.usuarioEmail
                        password = self.senhaEmail

                        msg = MIMEMultipart()
                        msg["From"] = emailfrom
                        msg["To"] = emailto
                        msg["Subject"] = "TESTE"
                        msg.preamble = "TESTE"
			
			nomes = open(self.nomeArquivoEmail, 'r+')
                        for linha in nomes:
                                if linha.strip() == '':
					continue
					print "E-mail enviado" 
				filename = linha.strip()
                                f = file(filename)
                                attachment = MIMEText(f.read())
                                attachment.add_header('Content-Disposition', 'attachment', filename=filename)
                                msg.attach(attachment)

                                server = smtplib.SMTP("64.233.186.109:587")
                                server.starttls()
                                server.login(user,password)
                        nomes.seek(0)
			nomes.truncate()
			nomes.close()
                        server.sendmail(emailfrom, emailto, msg.as_string())
                        server.quit()
                except socket.timeout:
                 print("Ocorreu um erro de Timeout do SMTP.")
		 time.sleep(10)
                 while 1:
                        if self.checkStatus() == False:
                                print "Sem rota para internet"
                                break
                        else:
                                self.conexaoEmail()
                                break

		 		
                except socket.error:
                 print("Oocorreu um erro de socket no SMTP. ")
		 time.sleep(10)
                 while 1:
		 	if self.checkStatus() == False:
                 		print "Sem rota para internet"
				break
		 	else:
				self.conexaoEmail()
				break


        def conexaoFtp(self):
                try:

                        sessao = ftplib.FTP(self.servidoFtp,self.loginFtp,self.senhaFtp)
                        nomes = open(self.nomeArquivoFtp,'r+')
                        for linha in nomes:
				if linha.strip() == '':
					print "Ftp envado"
					file.close()
					break
                                file = open(linha.strip(),'rb')
                                sessao.storbinary('STOR ' + linha.strip(), file)
			nomes.seek(0)
			nomes.truncate()
			nomes.close()
			#file.close()
                        sessao.quit()

                except socket.timeout:
                 print("Ocorreu um erro de Timeout do FTP.")
		 print("Ocorreu um erro de socket no FTP. ")
                 time.sleep(10)
                 while 1:
                        if self.checkStatus() == False:
                                print "Sem rota para internet"
                                break
                        else:
                                self.conexaoFtp()
                                break


		
                except socket.error:
                 print("Ocorreu um erro de socket no FTP. ")
                 time.sleep(10)
                 while 1:
                        if self.checkStatus() == False:
                                print "Sem rota para internet"
                                break
                        else:
                                self.conexaoFtp()
				break


        def conexaoHttp(self):
                try:
                        nomes = open(self.nomeArquivoHttp, 'rb')
                        for linha in nomes:
                                parametroTemperatura = linha.strip()
                                params = urllib.urlencode({'field1': parametroTemperatura,'key':'6BJJZ3EF157AIY1F'})
                                headers = {"Content-type": "application/x-www-form-urlencoded","Accept":  "text/plain"}
                                conn = httplib.HTTPConnection("184.106.153.149:80")
				conn.request("POST", "/update", params, headers)
                                response = conn.getresponse()
                                print response.status, response.reason
                                data = response.read()
                                time.sleep(30)
                        conn.close()


                except socket.timeout:
                 print ("Ocorreu um erro de Timeout do HTTP")

                except socket.error:
                 print ("Ocorreu um erro de Socket do HTTP")
