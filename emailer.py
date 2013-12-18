
import os,sys
from smtplib import SMTP_SSL as SMTP
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

def send(config,text,attch=[]):
	assert type(attch)==list
	
	msg = MIMEMultipart()
	me = config.xget('Email','from','emailer@orugaamarilla.com')
	myname = config.xget('Email','fromName','Oruga Amarilla emailer')
	to = config.xget('Email','address').split(';\n')
	server = config.xget('Email','server','mail.orugaamarilla.com')
	
	msg['From'] = "{} <{}>".format(myname,me)
	msg['To'] = ', '.join(to)
	msg['Date'] = formatdate(localtime=True)
	msg['Subject'] = config.xget('Email','subject',config.xget('Report','title'))
	
	msgtext = MIMEText(text)
	msg.attach(msgtext)
	
	for f in attch:
		attfile = MIMEBase('application','pdf')
		attfile.set_payload(open(f,'rb').read())
		Encoders.encode_base64(attfile)
		attfile.add_header('Content-Disposition', 'attachement; filename={}'.format(os.path.basename(f)))
		msg.attach(attfile)
	
	try:
		s = SMTP(server)
		s.set_debuglevel(0)
		s.login('emailer@orugaamarilla.com','1n73r:l3c70')
		try:
			s.sendmail(me, to, msg.as_string())
		finally:
			s.close()
	except Exception, exc:
		print "mail failed; %s" % str(exc)
