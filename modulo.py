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
import timeit

timeout = 900
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
                               
                        if self.checkStatus() == False:
                                print "Sem rota para Internet"

                        self.sendEnvio()
                        

	def run(self):
                self.gerenciaEnvio()

	
	def sendEnvio(self):
		self.conexaoEmail()
                self.conexaoFtp()
		
	
	def checkStatus(self):
                primeiroEth0 = os.system("ping -I eth0  -c 5 " + self.checkDestino )
                print "------------------------------------------------------------------------"
		segundaPpp0 = os.system("ping -I ppp0  -c 5 " + self.checkDestino )
		if primeiroEth0 == 0 or segundaPpp0  == 0:
                        print "Conexao Verifica e OK"
			print "------------------------------------------------------------------------"
                        return True
                else:
                        print "Conexao OFF"
                        return False


        def verificaInterface(self):
                        for dev in netinfo.list_active_devs():
                                 print dev
		
			if self.interfaceETH0 == dev:
				print "Interface Ativa"
				print "------------------------------------------------------------------------"
				return True


			if self.interfacePPP0 == dev:
				print "Interface Ativa"
				print "------------------------------------------------------------------------"
				return True

			else:
                                print "Sem Rota para internet"
                                return False
	

	def saidaSocketFTP(self):
        	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        	s.connect(("8.8.8.8",80))
        	print "Saindo FTP pelo", (s.getsockname()[0])
        	s.close()


	def saidaSocketSMTP(self):
        	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        	s.connect(("8.8.8.8",80))
        	print "Saindo SMTP pelo", (s.getsockname()[0])
        	s.close()

	

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
			
			server = smtplib.SMTP("64.233.186.109:587")
                        server.starttls()
                        server.login(user,password)


			nomes = open(self.nomeArquivoEmail, 'r+')
			start = timeit.default_timer()
			for linha in nomes:
				if linha.strip() =='':
					print "E-mail enviado" 
					break				
				
				filename = linha.strip()
                                f = file(filename)
                                attachment = MIMEText(f.read())
                        	attachment.add_header('Content-Disposition', 'attachment', filename=filename)
                        	msg.attach(attachment)
				

			nomes.seek(0)
			nomes.truncate()
                        self.saidaSocketSMTP()						
			server.sendmail(emailfrom, emailto, msg.as_string())
			stop = timeit.default_timer()			
			print stop - start
			nomes.close()
			server.quit()
                except socket.timeout:
                 print("Ocorreu um erro de Timeout do SMTP.")
		 time.sleep(1)
                 while 1:
                        if self.checkStatus() == False:
                                print "Sem rota para internet"
                                break
                        else:
                                self.conexaoEmail()
                                break

		 		
                except socket.error:
                 print("Oocorreu um erro de socket no SMTP. ")
		 time.sleep(1)
                 while 1:
			if self.checkStatus() == False:
                		print "Sem rota para internet"
				break
			else:
				self.conexaoEmail()
				break
		
	      
		except smtplib.SMTPException:
		 print "Ocorreu um erro durante o envio"


	def conexaoFtp(self):
                try:

                        sessao = ftplib.FTP(self.servidoFtp,self.loginFtp,self.senhaFtp)
                        nomes = open(self.nomeArquivoFtp,'r+')
			for linha in nomes:
				start = timeit.default_timer()
				if linha.strip() == '':
					print "Ftp envado"
					file.lose()
					break

				file = open(linha.strip(),'rb')
                        	sessao.storbinary('STOR ' + linha.strip(),file )
				stop = timeit.default_timer()
                        	print stop - start
			self.saidaSocketFTP()
			nomes.seek(0)
			nomes.truncate()
			nomes.close()
                        sessao.quit()

                except socket.timeout:
                 print("Ocorreu um erro de Timeout do FTP.")
                 time.sleep(1)
                 while 1:
                        if self.checkStatus() == False:
                                print "Sem rota para internet"
                                break
                        else:
                                self.conexaoFtp()
                                break


		
                except socket.error:
                 print("Ocorreu um erro de socket no FTP. ")
                 time.sleep(1)
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

