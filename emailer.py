
import os,sys,config
from smtplib import SMTP_SSL as SMTP
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

mtypes = {
	'cvs': ('text','cvs'),
	'doc': ('application','msword'),
	'docx': ('application','msword'),
	'gif': ('image','gif'),
	'htm': ('text','html'),
	'html': ('text','html'),
	'jpeg': ('image','jpeg'),
	'jpg': ('image','jpeg'),
	'js': ('application','javascript'),
	'json': ('application','json'),
	'pdf': ('application','pdf'),
	'png': ('image','png'),
	'xls': ('application','vnd.ms-excel'),
	'xlsx': ('application','vnd.ms-excel'),
}

def mimebase(filename):
	if filename.lower() in mtypes.keys():
		ext = filename.lower()
		return MIMEBase(mtypes[ext][0],mtypes[ext][1])
	i = filename.rfind('.')
	if i:
		ext = filename[i+1:].lower()
		if ext in mtypes.keys():
			return MIMEBase(mtypes[ext][0],mtypes[ext][1])
	return MIMEBase('application','octet-stream')

def mimetype(filename):
	if filename.lower() in mtypes.keys():
		ext = filename.lower()
		return "{}/{}".format(mtypes[ext][0],mtypes[ext][1])
	i = filename.rfind('.')
	if i:
		ext = filename[i+1:].lower()
		if ext in mtypes.keys():
			return "{}/{}".format(mtypes[ext][0],mtypes[ext][1])
	return 'application/octet-stream'

def nsend(text,attch=[]):
	print text

def send(text,attch=[]):
	assert type(attch)==list
	
	msg = MIMEMultipart()
	me = config.get('Email','from','emailer@orugaamarilla.com')
	myname = config.get('Email','from name','Oruga Amarilla emailer')
	to = config.getlist('Email','address')
	server = config.get('Email','server','mail.orugaamarilla.com')
	
	msg['From'] = "{} <{}>".format(myname,me)
	msg['To'] = ', '.join(to)
	msg['Date'] = formatdate(localtime=True)
	msg['Subject'] = config.get('Email','subject',config.get('Report','title'))
	
	msgtext = MIMEText(text.encode('Latin-1'))
	msg.attach(msgtext)
	
	for f in attch:
		attfile = mimebase(f)
		attfile.set_payload(open(f,'rb').read())
		Encoders.encode_base64(attfile)
		attfile.add_header('Content-Disposition', 'attachement; filename={}'.format(os.path.basename(f)))
		msg.attach(attfile)

	try:
		import base64
		user = config.get('Email','user')
		if user is None:
			user = me
		passwd = base64.b64decode(config.get('Email','key'))
	finally:
		pass

	try:
		s = SMTP(server)
		s.set_debuglevel(0)
		s.login(user,passwd)
		try:
			s.sendmail(me, to, msg.as_string())
		finally:
			s.close()
	except Exception, exc:
		config.close()
		print "mail failed; %s" % str(exc)
