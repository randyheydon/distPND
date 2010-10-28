from distutils.core import Command
from xml.dom.minidom import Document


class gen_pxml(Command):
	
	user_options = [
		('outfile=', None,
		'specify where to put the resulting xml data'),
		('id=', None,
		'specify the unique id to use for this application (default is based on name from setup function)'),
		('appdata=', None,
		'specify the name of the appdata directory (default is same as id)'),
		('title=', None,
		'specify a title (default is name from setup function)'),
		('description=', None,
		'specify a description for the program (default is from setup function)'),
		('icon=', None,
		'specify an icon file to use'),
		('info=', None,
		'specify a help file to use'),
		('previewpics=', None,
		'specify any comma-separated preview pictures to use'),
		('author=', None,
		'specify the author (default is from setup function)'),
		('author-email=', None,
		"specify the author's email (default is from setup function)"),
		('author-website=', None,
		"specify the author's website (default is url from setup function)"),
		('version=', None,
		'specify the package version (default is from setup function)'),
		('osversion=', None,
		'specify the required OS version, if any'),
		('clockspeed=', None,
		'specify the required system clock, in Hz, if needed'),
		('mkdir=', None,
		"specify comma-separated folders to create on the SD root, but don't use it, okay?"),
		#categories, associations
	]


	def initialize_options(self):
		self.outfile = 'PXML.xml'
		self.id = None
		self.appdata = None
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
		if self.id is None:
			self.id = self.title.lower().replace(' ','-')
		
		if self.appdata is None:
			self.appdata = self.id
		
		#autogen exec lines or something?
		
		#check icon exists, else warn and change to none.
		
		if self.info is not None:
			#check info exists, else warn and change to none.
			from mimetypes import guess_type
			self.info_type = guess_type(self.info)[0]
			if self.info_type not in ('text/plain', 'text/html'):
				self.warn("Don't recognize info file extension.  Will assume text/plain")
				self.info_type = 'text/plain'
		
		#check previewpics exist, else warn and change to none.
		if self.previewpics is not None:
			self.previewpics = self.previewpics.split(',')
		
		#Need to fail if version does not exist.
		self.version = self.version.split('.')
		if len(self.version) > 4:
			self.warn('Version number has too many dot-separated segments.  Only first four will be used.')
		self.version.extend(('0','0','0','0')) #Ensure at least four subterms.
		
		if self.osversion is not None:
			self.osversion = self.osversion.split('.')
			if len(self.osversion) > 4:
				self.warn('OS version number has too many dot-separated segments.  Only first four will be used.')
			self.osversion.extend(('0','0','0','0')) #Ensure at least four subterms.
		
		#What do about categories?
		
		#What do about associations?
		
		if self.clockspeed is not None and not self.clockspeed.isdigit():
			self.warn('Your Pandora might not like a non-integer clockspeed.')
		
		if self.mkdir is not None:
			self.warn("Don't use mkdir.  Please.")
			self.mkdir = self.mkdir.split(',')


	def run(self):
		doc = Document()
		pxml = doc.createElement('PXML')
		doc.appendChild(pxml)
		pxml.setAttribute('xmlns','http://openpandora.org/namespaces/PXML')

		app = doc.createElement('application')
		pxml.appendChild(app)
		app.setAttribute('id', self.id)
		app.setAttribute('appdata', self.appdata)

		title = doc.createElement('title')
		app.appendChild(title)
		title.setAttribute('lang', 'en_US')
		title.appendChild(doc.createTextNode(self.title))

		description = doc.createElement('description')
		app.appendChild(description)
		description.setAttribute('lang', 'en_US')
		description.appendChild(doc.createTextNode(self.description))

		ex = doc.createElement('exec')
		app.appendChild(ex)
		ex.setAttribute('command', self.distribution.scripts[0])
		#There are many other attributes to exec that are being ignored.
		#Add user_options for them?  Or make them write their own PXML?
		#Also, what to do about multiple scripts?

		if self.icon is not None:
			icon = doc.createElement('icon')
			app.appendChild(icon)
			icon.setAttribute('src', self.icon)

		if self.info is not None:
			info = doc.createElement('info')
			app.appendChild(info)
			info.setAttribute('name', '%s help'%self.title)
			info.setAttribute('src', self.info)
			info.setAttribute('type', self.info_type)

		if self.previewpics is not None:
			ppics = doc.createElement('previewpics')
			app.appendChild(ppics)
			for i in self.previewpics:
				pic = doc.createElement('pic')
				ppics.appendChild(pic)
				pic.setAttribute('src', i)

		author = doc.createElement('author')
		app.appendChild(author)
		if self.author != 'UNKNOWN':
			author.setAttribute('name', self.author)
		if self.author_website != 'UNKNOWN':
			author.setAttribute('website', self.author_website)
		if self.author_email != 'UNKNOWN':
			author.setAttribute('email', self.author_email)

		version = doc.createElement('version')
		app.appendChild(version)
		version.setAttribute('major', self.version[0])
		version.setAttribute('minor', self.version[1])
		version.setAttribute('release', self.version[2])
		version.setAttribute('build', self.version[3])
		
		if self.osversion is not None:
			osversion = doc.createElement('osversion')
			app.appendChild(osversion)
			osversion.setAttribute('major', self.osversion[0])
			osversion.setAttribute('minor', self.osversion[1])
			osversion.setAttribute('release', self.osversion[2])
			osversion.setAttribute('build', self.osversion[3])

		if self.categories is not None:
			#What do about categories??
			pass

		if self.associations is not None:
			#What do about associations??
			pass

		if self.clockspeed is not None:
			clockspeed = doc.createElement('clockspeed')
			app.appendChild(clockspeed)
			clockspeed.setAttribute('frequency', self.clockspeed)

		if self.mkdir is not None:
			mkdir = doc.createElement('mkdir')
			app.appendChild(mkdir)
			for i in self.mkdir:
				dirr = doc.createElement('dir')
				mkdir.appendChild(dirr)
				dirr.setAttribute('path', i)


		#Now that XML is all generated, write it to the specified file.
		outfile = open(self.outfile, 'w')
		try: outfile.write(doc.toprettyxml())
		finally: outfile.close()
