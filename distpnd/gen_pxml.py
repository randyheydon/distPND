from distutils.core import Command
from distutils.errors import DistutilsOptionError
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
		('exec-command=', None,
		'specify the command executed by the PND (default is first script listed in setup function; only one command is supported for now)'),
		('exec-args=', None,
		'specify any arguments to be passed to the command specified by "exec"'),
		('exec-startdir=', None,
		'specify the directory in which the command should be started (default is the root of the PND file)'),
		#('exec-nostandalone', None,
		#"activate this flag if the command should only be run with associations.  Since those aren't implemented yet, just don't use this flag"),
		('exec-nobackground', None,
		'activate this flag if users should not be able to switch applications while this is running'),
		('exec-nox', None,
		'activate this flag if the command should not be run in an X environment'),
		('exec-xreq', None,
		'activate this flag if the command requires an X environment to run'),
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
		('categories=', None,
		'specify any comma-separated top-level categories to which this belongs'),
		#('associations=', None,
		#"I don't even think this is implemented in libpnd, so I won't have it here."),
		('clockspeed=', None,
		'specify the required system clock, in Hz, if needed'),
		('mkdir=', None,
		"specify comma-separated folders to create on the SD root, but don't use it, okay?"),
	]


	def initialize_options(self):
		self.outfile = 'PXML.xml'
		self.id = None
		self.appdata = None
		self.title = self.distribution.get_name()
		self.description = self.distribution.get_description()
		self.exec_command = None
		self.exec_args = None
		self.exec_startdir = None
		self.exec_nostandalone = False
		self.exec_nobackground = False
		self.exec_nox = False
		self.exec_xreq = False
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
			#Should ensure id and appdata have no invalid filename characters.
			self.id = self.title.lower().replace(' ','-')
		
		if self.appdata is None:
			self.appdata = self.id
		
		if self.title == 'UNKNOWN':
			raise DistutilsOptionError('No name was found in the setup script and no title was specified.  You need one of these.')

		if self.description == 'UNKNOWN':
			self.warn('No description was found in the setup script or specified.  You should have one of these.')

		#autogen exec lines or something?
		if self.exec_command is None:
			try: self.exec_command = self.distribution.scripts[0]
			except TypeError:
				raise DistutilsOptionError('Either your setup function should specify at least one script (in list format), or you should specify it as an option.  What is your PND going to run?')

		if self.exec_nox and self.exec_xreq:
			raise DistutilsOptionError('You can require X or you can require no X, but how am I supposed to satisfy both?  Please pick only one.')
		
		#check icon exists, else warn and change to none.
		#also check icon is a valid format
		
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
		if self.version == '0.0.0': #This happens when version is not in setup script.
			self.warn('No version number is specified.  All zeros will be inserted.')
		self.version = self.version.split('.')
		if len(self.version) > 4:
			self.warn('Version number has too many dot-separated segments.  Only first four will be used.')
		self.version.extend(('0','0','0','0')) #Ensure at least four subterms.
		
		if self.osversion is not None:
			self.osversion = self.osversion.split('.')
			if len(self.osversion) > 4:
				self.warn('OS version number has too many dot-separated segments.  Only first four will be used.')
			self.osversion.extend(('0','0','0','0')) #Ensure at least four subterms.
		
		if self.categories is not None:
			self.categories = self.categories.split(',')
			for i in self.categories:
				if i not in ('AudioVideo', 'Audio', 'Video', 'Development', 'Education',
					'Game', 'Graphics', 'Network', 'Office', 'Settings', 'System', 'Utility'):
					self.warn('%s is not a valid top-level FreeDesktop category.  It will still be added to your PND, but you should only use categories found at http://standards.freedesktop.org/menu-spec/latest/apa.html' % i)
		
		#if self.associations is not None:
			#Do something with associations.
		
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
		ex.setAttribute('command', self.exec_command)
		if self.exec_args is not None:
			ex.setAttribute('arguments', self.exec_args)
		if self.exec_startdir is not None:
			ex.setAttribute('startdir', self.exec_startdir)
		if self.exec_nostandalone:
			ex.setAttribute('standalone', 'false')
		else:
			ex.setAttribute('standalone', 'true')
		if self.exec_nobackground:
			ex.setAttribute('background', 'false')
		else:
			ex.setAttribute('background', 'true')
		if self.exec_nox:
			ex.setAttribute('x11', 'stop')
		elif self.exec_xreq:
			ex.setAttribute('x11', 'req')

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
			categories = doc.createElement('categories')
			app.appendChild(categories)
			for i in self.categories:
				category = doc.createElement('category')
				categories.appendChild(category)
				category.setAttribute('name', i)

		#if self.associations is not None:
			#What do about associations??

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
		#Instead use self.make_file?
		outfile = open(self.outfile, 'w')
		try: outfile.write(doc.toprettyxml())
		finally: outfile.close()
