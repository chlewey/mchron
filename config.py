
import ConfigParser

class mcConfig(ConfigParser.ConfigParser):
	def __init__(self,filename=False):
		ConfigParser.ConfigParser.__init__(self)
		self.filename = filename or 'config.cfg'
		self.read(self.filename)
		
	def __enter__(self):
		return self
		
	def __exit__(self, type, value, traceback):
		with open(self.filename, 'w') as fp:
			self.write(fp)

	def xget(self, section, option, default=None):
		if self.has_section(section):
			if self.has_option(section, option):
				return self.get(section, option)
		elif default is not None:
			self.add_section(section)
		if default is not None:
			self.set(section,option,default)
		return default
	
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
