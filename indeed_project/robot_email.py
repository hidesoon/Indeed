#add ability to send an email when the extraction is done from separate computer

import smtplib

def send(message):
	try:
		server = smtplib.SMTP('smtp.gmail.com','587')
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login('fromEmail@gmail.com','#####')
		server.sendmail('fromEmail@gmail.com','toEmail@gmail.com',message)
		server.close()
	except:
		print "Failed to send e-mail."

		
