# DataStructures.py



class Domain():

	"""docstring for Domain"""
	def __init__(self, name):
		super(Domain, self).__init__()
		self.name = name
		self.libraries = []

	def addLibrary(self, library):
		self.libraries.append(library)

	def getLibrary(self, index):
		return self.libraries[index]

	def getName(self):
		return self.name

	@staticmethod
	def arrayContainsWithName(array, name):
		for domain in array:
			if domain.name == name:
				return domain

		return None

	def containsLibraryWithName(self, name):
		for library in self.libraries:
			if library.name == name:
				return library

		return None



class Library():

	def __init__(self, name):
		super(Library, self).__init__()
		self.name = name
		self.gitHubRepository = ""

		self.popularity = 0
		self.releaseDates = []
		self.lastModificationDate = None
		self.breakingChangesPerRelease = []
		self.lastDiscussedOnStackOverflow = None
		self.questionsAsked = 0
		self.issues = []



class Issue():


	def __init__(self):
		super(Issue, self).__init__()
		self.id = 0
		self.creationDate = None
		self.closingDate = None
		self.firstCommentDate = None
		self.performance = False
		self.security = False






		