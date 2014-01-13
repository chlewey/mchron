
import ConfigParser

class mcConfig(ConfigParser.ConfigParser):
	def __init__(self,filename=False):
		ConfigParser.ConfigParser.__init__(self)
		self.filename = filename or 'config.cfg'
		self.read(self.filename)
	
	def __str__(self):
		s = ''
		for x in self.sections():
			s += '['+x+']\n'
			for y in self.options(x):
				try:
					s += y+' = '+self.get(x,y)+'\n'
				except:
					print s,('ERROR IN:',x,y),'\n\n'
			s += '\n'
		return s
		
	def __enter__(self):
		return self
		
	def __exit__(self, type, value, traceback):
		self.close()
	
	def save(self):
		with open(self.filename, 'w') as fp:
			self.write(fp)

	def close(self):
		self.save()

	def remove(self, section, option):
		if self.has_section(section):
			self.remove_option(section, option)
		else:
			self.add_section(section)

	def xget(self, section, option, default=None):
		if self.has_section(section):
			if self.has_option(section, option):
				answer = self.get(section, option)
				return answer
		elif default is not None:
			self.add_section(section)
		if default is not None:
			self.set(section,option,default)
		return default
		
	def getlist(self, section, option):
		if self.has_section(section):
			if self.has_option(section, option):
				return self.get(section, option).split(';\n')
		return []

	def setlist(self, section, option, data):
		assert type(data)==list
		self.xset(section,option,';\n'.join(data))

	def addtolist(self, section, option, item):
		l = self.getlist(section, option)
		l.append(item)
		self.setlist(section, option, l)
	
	def xset(self, section, option, value):
		if not self.has_section(section):
			self.add_section(section)
		self.set(section, option, value)

	def check(self, section, option, value, replace=False):
		if self.has_section(section):
			if self.has_option(section, option):
				result = self.get(section, option)
				if result != value and replace:
					self.set(section,option,value)
				return result
		else:
			self.add_section(section)
		self.set(section, option, value)
		return False

	def checklist(self, section, option, data, replace=False):
		assert hasattr(data, '__iter__')
		value = ';\n'.join(data)
		result = self.check(section, option, value, replace)
		if type(result)==bool:
			return result
		return result.split(';\n')
		
__config = None

def init(configfile):
	global __config
	__config = mcConfig(configfile)

def get(section, option, default=None):
	global __config
	return __config.xget(section, option, default)

def set(section, option, value):
	global __config
	return __config.xset(section, option, value)

def check(section, option, value, replace=False):
	global __config
	return __config.check(section, option, value, replace)

def checklist(section, option, data, replace=False):
	global __config
	return __config.checklist(section, option, data, replace)

def setlist(section, option, data):
	global __config
	return __config.setlist(section, option, data)

def getlist(section, option):
	global __config
	return __config.getlist(section, option)

def addtolist(section, option, item):
	global __config
	return __config.addtolist(section, option, item)

def remove(section, option):
	global __config
	return __config.remove(section, option)

def save():
	global __config
	__config.save()

def close():
	global __config
	__config.close()

if __name__ == "__main__":
	import sys,os.path,shutil
	if 'xp' in sys.argv:
		osys = 'winxp'
	else:
		osys = 'win7'
	template = osys+'.cfg'
	cfgfile = 'mchron.cfg'
	
	if os.path.exists(template) and not os.path.exists(cfgfile):
		shutil.copyfile(template,cfgfile)
		
	init(cfgfile)
	check('Database','maker','sitrad')
	check('Database','source','datos.db')
	if 'local' in sys.argv:
		check('Database','path','.',True)
	for arg in sys.argv:
		if '@' in arg:
			addtolist('Email', 'address', arg)
		elif arg[:-3]=='.db':
			check('Database','source',arg,True)
	from base64 import b64encode
	check('Email','key',b64encode('1n74r:l3c70'))
	close()
