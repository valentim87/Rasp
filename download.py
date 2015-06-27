from modulo import *
import email, getpass, imaplib, os
import hashlib

detach_dir = '/root/projeto/gmail' 
	
user = 'agrotic.ufrpe@gmail.com'
pwd = 'agroaco2014'

m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login(user,pwd)

m.select("[Gmail]/Todos os e-mails") 

resp, items = m.search(None, "ALL") 
items = items[0].split() 

for emailid in items:
    	resp, data = m.fetch(emailid, "(RFC822)") 

    	email_body = data[0][1] # 
    	mail = email.message_from_string(email_body) 

   	if mail.get_content_maintype() != 'multipart':
       		continue
 
   	print "["+mail["From"]+"] :" + mail["Subject"]
		
		
    	for part in mail.walk():
        	if part.get_content_maintype() == 'multipart':
            		continue

       
        	if part.get('Content-Disposition') is None:
            		continue

        	filename = part.get_filename()
		counter = 1

		escrevemail = open('/root/projeto/gmail/listafora.txt','r+')
                old = escrevemail.read()
                escrevemail.seek(0)
                escrevemail.write(str(filename +'\n' +old ))
		escrevemail.close()

			
        	if not filename:
            		filename = 'part-%03d%s' % (counter, 'bin')
            		counter += 1

        	att_path = os.path.join(detach_dir, filename)
    	
		if not os.path.isfile(att_path) :
            		fp = open(att_path, 'wb')
            		fp.write(part.get_payload(decode=True))
            		fp.close()


server = '31.170.162.143'
username = 'a5694651'
password = 'thiago123456'
 
directory = '/'
filematch = '*.dat'

os.chdir("/root/projeto/ftp") 

ftp = ftplib.FTP(server)
ftp.login(username, password)
 
ftp.cwd(directory)
 
for filename in ftp.nlst(filematch):
	fhandle = open(filename, 'wb')
	print 'Getting ' + filename
	ftp.retrbinary('RETR ' + filename, fhandle.write)
    	escreveftp = open('/root/projeto/ftp/listafora.txt','r+')
        old = escreveftp.read()
       	escreveftp.seek(0)
        escreveftp.write(str(filename +'\n' +old ))
        escreveftp.close()
	fhandle.close()

finalSMTP = []	
listaA = []
listaB = []
listaC = []
listafora = open('/root/projeto/gmail/listafora.txt','r+')
listadentro = open('/root/projeto/listadentro.txt','r+')
for arquivofora in listafora:
	if arquivofora == '\n':
                break
	h = hashlib.md5()
	h.update(arquivofora)
	p = h.hexdigest()
	listaA.append(p)
for arquivodentro in listadentro:
	t = hashlib.md5()
        t.update(arquivodentro)
        k = t.hexdigest()
        listaB.append(k)

for i in listaA:
	for j in listaB:
		if i == j:
			listaC.append(j)

finalSMTP = (set(listaC))
print "Verificamos a integridade dos arquivos do protocolo SMTP de 68 enviados: " , len(finalSMTP) ," Chegaram integros."


finalFTP = []		
listaD = []
listaE = []
listaF = [] 
listaforaftp = open('/root/projeto/ftp/listafora.txt','r+')
listadentroftp = open('/root/projeto/listadentro.txt','r+')
for arquivoforaftp in listaforaftp:
	if arquivoforaftp == '\n':
       		break
	h = hashlib.md5()
       	h.update(arquivoforaftp)
       	i = h.hexdigest()
       	listaD.append(i)
for arquivodentroftp in listadentroftp:
       w = hashlib.md5()
       w.update(arquivodentroftp)
       z = w.hexdigest()
       listaE.append(z)

for i in listaD:
       for j in listaE:
               if i == j:
                       listaF.append(j)
finalFTP = list(set(listaF))


print "Verificamos a integridade dos arquivos do protocolo FTP de 68 enviados: ", len(finalFTP) ," Chegaram integros."
