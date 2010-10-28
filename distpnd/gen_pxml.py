from distutils.core import Command
from xml.dom.minidom import Document


class gen_pxml(Command):
	
	user_options = [
		('outfile=', None,
		'specify where to put the resulting xml data'),
		('title=', None,
		'specify a title (default is taken from setup function)'),
		('icon=', None,
		'specify an icon file to use'),
		('info=', None,
		'specify a help file to use'),
		('previewpics=', None,
		'specify any comma-separated preview pictures to use'),
		('version=', None,
		'specify the package version (default is taken from setup function)'),
		#osversion, categories, associations, clockspeed...
		#and any options that can be read from setup should be overrideable
	]


	def initialize_options(self):
		self.outfile = 'PXML.xml'
		self.title = self.distribution.get_name()
		self.description = self.distribution.get_description()
		#exec?
		self.icon = None
		self.info = None
		self.previewpics = None
		self.author = self.distribution.get_author()
		self.author_email = self.distribution.get_author_email()
		self.author_website = self.distribution.get_url()
		self.version = self.distribution.get_version()
		self.osversion = None
		self.categories = None
		self.associations = None
		self.clockspeed = None
		self.mkdir = None
	

	def finalize_options(self):
		#autogen exec lines or something?
		#check icon exists, else warn and change to none.
		#check info exists, else warn and change to none.
		#check previewpics exist, else warn and change to none.
		self.version = self.version.split('.')
		if len(self.version) > 4:
			self.warn('Version number has too many dot-separated segments.  Only first four will be used.')
		self.version = self.version[:4]
		#Should probably make similar check on osversion.
		#What do about categories?
		#What do about associations?
		if self.clockspeed is not None:
			try: self.clockspeed = int(self.clockspeed)
			except TypeError:
				self.warn('Your Pandora might not like a non-integer clockspeed.')
		if self.mkdir is not None:
			self.warn("Don't use mkdir.  Please.")


	def run(self):
		print self.version
		doc = Document()
		pxml = doc.createElement('PXML')
		doc.appendChild(pxml)
		pxml.setAttribute('xmlns','http://openpandora.org/namespaces/PXML')
		#print doc.toprettyxml(indent="	")
