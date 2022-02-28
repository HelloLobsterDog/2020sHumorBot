import logging
import os
import os.path
import random

from .ObjectDetector import ObjectDetector
from .ImageTweeter import ImageTweeter
from .Distorter import Distorter
from .ImageCaptioner import ImageCaptioner
from .NameStupifier import NameStupifier

class TwentyTwentiesHumorBot(object):
	def __init__(self, homeDir, tries = 3):
		self.homeDir = homeDir
		self.tries = tries
		self.logger = logging.getLogger('2020sHumorBot')
		
		self.inputImageDirName = 'input'
		self.identifiedImageDirName = 'identified'
		self.bulgedDirName = 'bulged'
		self.labeledDirName = 'output'
		self.usedDirName = 'used'
		self.failedDirName = 'failed'
		
		self.curationDirName = 'curation'
		self.successDirName = 'successful'
		
		self.detector = ObjectDetector(self.homeDir)
		self.distorter = Distorter(self.homeDir)
		self.stupifier = NameStupifier()
		self.captioner = ImageCaptioner(self.homeDir)
		
	def run(self):
		try:
			self.validateHomeDir()
			
			for attempt in range(self.tries):
				image = self.pickImage()
				try:
					objectInImage = self.detector.objectIdentification(image, os.path.join(self.homeDir, self.identifiedImageDirName))
					distortedImage = self.distorter.distort(image, os.path.join(self.homeDir, self.bulgedDirName), objectInImage)
					stupifiedName = self.stupifier.stupify(objectInImage.name)
					distortedLabeledImage = self.captioner.writeText(distortedImage, os.path.join(self.homeDir, self.labeledDirName), stupifiedName)
				except Exception as e:
					self.logger.exception("Encountered exception while attempting to process image: " + image)
					self.markImageAsFailed(image)
					continue
				ImageTweeter(self.homeDir).tweetImage(distortedLabeledImage)
				self.markImageAsUsed(image)
				break
			
			return True
			
		except Exception as e:
			self.logger.exception("Encountered an exception while attempting to run.")
			return False
			
	def runCuration(self):
		path = os.path.join(self.homeDir, self.curationDirName, self.inputImageDirName)
		anyFailures = False
		for filename in os.listdir(path):
			imagePath = os.path.join(self.homeDir, self.curationDirName, self.inputImageDirName, filename)
			self.logger.info("running curation on image at path: " + imagePath)
			try:
				objectInImage = self.detector.objectIdentification(imagePath, os.path.join(self.homeDir, self.curationDirName, self.identifiedImageDirName))
				distortedImage = self.distorter.distort(imagePath, os.path.join(self.homeDir, self.curationDirName, self.bulgedDirName), objectInImage)
				stupifiedName = self.stupifier.stupify(objectInImage.name)
				distortedLabeledImage = self.captioner.writeText(distortedImage, os.path.join(self.homeDir, self.curationDirName, self.labeledDirName), stupifiedName)
				self.markImageAsUsedCuration(imagePath)
			except Exception as e:
				self.logger.exception("Encountered exception while attempting to process image: " + imagePath)
				self.markImageAsFailedCuration(imagePath)
				anyFailures = True
				continue
		return not anyFailures
		
		
		
	def validateHomeDir(self):
		pass # TODO
		
	def pickImage(self):
		path = os.path.join(self.homeDir, self.inputImageDirName)
		filesInDir = os.listdir(path)
		if not filesInDir:
			raise RuntimeError("input image directory is empty.")
		picked = os.path.join(self.homeDir, self.inputImageDirName, random.choice(filesInDir))
		self.logger.info("Picked image: %s", picked)
		return picked
		
	def markImageAsUsed(self, path):
		pathToMoveTo = os.path.join(self.homeDir, self.usedDirName, os.path.basename(path))
		os.rename(path, pathToMoveTo)
		self.logger.info("image %s moved to used folder: %s", path, pathToMoveTo)
		
	def markImageAsFailed(self, path):
		pathToMoveTo = os.path.join(self.homeDir, self.failedDirName, os.path.basename(path))
		os.rename(path, pathToMoveTo)
		self.logger.info("image %s moved to failed folder: %s", path, pathToMoveTo)
		
	def markImageAsUsedCuration(self, path):
		pathToMoveTo = os.path.join(self.homeDir, self.curationDirName, self.successDirName, os.path.basename(path))
		os.rename(path, pathToMoveTo)
		self.logger.info("image %s moved to success folder: %s", path, pathToMoveTo)
		
	def markImageAsFailedCuration(self, path):
		pathToMoveTo = os.path.join(self.homeDir, self.curationDirName, self.failedDirName, os.path.basename(path))
		os.rename(path, pathToMoveTo)
		self.logger.info("image %s moved to failed folder: %s", path, pathToMoveTo)
