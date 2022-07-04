import logging
import os
import os.path
import random

from .ObjectDetector import ObjectDetector
from .ImageTweeter import ImageTweeter
from .Distorter import Distorter
from .ImageCaptioner import ImageCaptioner
from .NameStupifier import NameStupifier
from .FileHandler import FileHandler

class TwentyTwentiesHumorBot(object):
	def __init__(self, homeDir, tries = 3):
		self.homeDir = homeDir
		self.tries = tries
		self.logger = logging.getLogger('2020sHumorBot')
		self.rand = random.Random()
		
		self.detector = ObjectDetector(self.homeDir)
		self.distorter = Distorter(self.homeDir, self.rand)
		self.stupifier = NameStupifier(self.rand)
		self.captioner = ImageCaptioner(self.homeDir)
		self.imageTweeter = ImageTweeter(self.homeDir)
		self.fileHandler = FileHandler(self.homeDir)
		
	def run(self):
		try:
			self.validateHomeDir()
			
			for attempt in range(self.tries):
				imagePath = self.fileHandler.pickImage()
				self.initializeRandom(imagePath)
				try:
					objectInImage = self.detector.objectIdentification(imagePath, self.fileHandler.identifiedDir)
					distortedImage = self.distorter.distort(imagePath, self.fileHandler.distortedDir, objectInImage)
					stupifiedName = self.stupifier.stupify(objectInImage.name)
					distortedLabeledImage = self.captioner.writeText(distortedImage, self.fileHandler.labeledDir, stupifiedName)
				except Exception as e:
					self.logger.exception("Encountered exception while attempting to process image: " + imagePath)
					self.fileHandler.markImageAsFailed(imagePath)
					continue
				self.imageTweeter.tweetImage(distortedLabeledImage)
				self.fileHandler.markImageAsUsed(imagePath)
				return True
			
		except Exception as e:
			self.logger.exception("Encountered an exception while attempting to run.")
		return False
			
	def runCuration(self):
		anyFailures = False
		for filename in self.fileHandler.curationPaths():
			self.initializeRandom(filename)
			imagePath = os.path.join(self.fileHandler.inputDirCuration, filename)
			self.logger.info("running curation on image at path: " + imagePath)
			try:
				objectInImage = self.detector.objectIdentification(imagePath, self.fileHandler.identifiedDirCuration)
				distortedImage = self.distorter.distort(imagePath, self.fileHandler.distortedDirCuration, objectInImage)
				stupifiedName = self.stupifier.stupify(objectInImage.name)
				distortedLabeledImage = self.captioner.writeText(distortedImage, self.fileHandler.labeledDirCuration, stupifiedName)
				self.fileHandler.markImageAsUsedCuration(imagePath)
			except Exception as e:
				self.logger.exception("Encountered exception while attempting to process image: " + imagePath)
				self.fileHandler.markImageAsFailedCuration(imagePath)
				anyFailures = True
		return not anyFailures
		
		
		
	def validateHomeDir(self):
		pass # TODO
		
		
		
	def initializeRandom(self, imagePath):
		filename = os.path.basename(imagePath)
		firstSection = filename.split(" ", 1)[0]
		try:
			number = int(firstSection)
		except Exception as e:
			if self.logger.isEnabledFor(logging.DEBUG):
				self.logger.exception("exception encountered while attempting to make string into an integer: %s This exception will be ignored, using 1 as the number.", firstSection)
			number = 1
		self.rand.seed()
		