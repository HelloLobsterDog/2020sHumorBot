import os
import os.path
import logging
import random

class FileHandler(object):
	def __init__(self, homeDir):
		self.logger = logging.getLogger('2020sHumorBot').getChild('FileHandler')
		
		self.homeDir = homeDir
		
		self.inputImageDirName = 'input'
		self.identifiedImageDirName = 'identified'
		self.distoredDirName = 'bulged'
		self.labeledDirName = 'output'
		self.usedDirName = 'used'
		self.failedDirName = 'failed'
		
		self.curationDirName = 'curation'
		self.successDirName = 'successful'
		
		
		
	def pickImage(self):
		path = os.path.join(self.homeDir, self.inputImageDirName)
		if not os.path.exists(path):
			raise RuntimeError("input image directory does not exist: " + path)
		filesInDir = os.listdir(path)
		if not filesInDir:
			raise RuntimeError("input image directory is empty.")
		picked = os.path.join(self.homeDir, self.inputImageDirName, random.choice(filesInDir))
		self.logger.info("Picked image: %s", picked)
		# setup intermediate directories
		os.makedirs(self.identifiedDir, exist_ok = True)
		os.makedirs(self.distortedDir, exist_ok = True)
		os.makedirs(self.labeledDir, exist_ok = True)
		return picked
		
	def markImageAsFailed(self, path):
		pathToMoveTo = os.path.join(self.homeDir, self.failedDirName, os.path.basename(path))
		os.makedirs(os.path.join(self.homeDir, self.failedDirName), exist_ok = True)
		os.rename(path, pathToMoveTo)
		self.logger.info("image %s moved to failed folder: %s", path, pathToMoveTo)
		
	def markImageAsUsed(self, path):
		currentFilename = os.path.basename(path)
		# increment the number in the name to get a different result next time
		splitName = path.split(" ", 1)
		firstSection = splitName[0]
		if len(splitName) > 1:
			secondSection = splitName[1]
		else:
			# no spaces in the name.
			firstSection = ""
			secondSection = splitName[0]
		try:
			number = int(firstSection)
		except Exception as e:
			if self.logger.isEnabledFor(logging.DEBUG):
				self.logger.exception("exception encountered while attempting to make string into an integer: %s This exception will be ignored, using 1 as the number.", firstSection)
			number = 0
			secondSection = " - " + currentFilename # The first section is not a number, so we're going to add a number to the original filename for them, instead of just incrementing
		number += 1
		incrementedFilename = str(number) + secondSection
		# move
		pathToMoveTo = os.path.join(self.homeDir, self.usedDirName, incrementedFilename)
		os.makedirs(os.path.join(self.homeDir, self.usedDirName), exist_ok = True)
		os.rename(path, pathToMoveTo)
		self.logger.info("image %s moved to used folder: %s", path, pathToMoveTo)
		
	@property
	def identifiedDir(self):
		return os.path.join(self.homeDir, self.identifiedImageDirName)
		
	@property
	def distortedDir(self):
		return os.path.join(self.homeDir, self.distoredDirName)
		
	@property
	def labeledDir(self):
		return os.path.join(self.homeDir, self.labeledDirName)
		
		
	
	def curationPaths(self):
		if not os.path.exists(self.inputDirCuration):
			raise RuntimeError("Curation input image directory does not exist: " + path)
		# setup intermediate directories
		os.makedirs(self.identifiedDirCuration, exist_ok = True)
		os.makedirs(self.distortedDirCuration, exist_ok = True)
		os.makedirs(self.labeledDirCuration, exist_ok = True)
		# get the images
		for filename in os.listdir(self.inputDirCuration):
			yield filename
		
	def markImageAsUsedCuration(self, path):
		pathToMoveTo = os.path.join(self.homeDir, self.curationDirName, self.successDirName, os.path.basename(path))
		os.makedirs(os.path.join(self.homeDir, self.curationDirName, self.successDirName), exist_ok = True)
		os.rename(path, pathToMoveTo)
		self.logger.info("image %s moved to success folder: %s", path, pathToMoveTo)
		
	def markImageAsFailedCuration(self, path):
		pathToMoveTo = os.path.join(self.homeDir, self.curationDirName, self.failedDirName, os.path.basename(path))
		os.makedirs(os.path.join(self.homeDir, self.curationDirName, self.failedDirName), exist_ok = True)
		os.rename(path, pathToMoveTo)
		self.logger.info("image %s moved to failed folder: %s", path, pathToMoveTo)
		
	@property
	def inputDirCuration(self):
		return os.path.join(self.homeDir, self.curationDirName, self.inputImageDirName)
		
	@property
	def identifiedDirCuration(self):
		return os.path.join(self.homeDir, self.curationDirName, self.identifiedImageDirName)
		
	@property
	def distortedDirCuration(self):
		return os.path.join(self.homeDir, self.curationDirName, self.distoredDirName)
		
	@property
	def labeledDirCuration(self):
		return os.path.join(self.homeDir, self.curationDirName, self.labeledDirName)