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
	def __init__(self, homeDir):
		self.homeDir = homeDir
		self.logger = logging.getLogger('2020sHumorBot')
		
		self.inputImageDirName = 'input'
		self.identifiedImageDirName = 'identified'
		self.bulgedDirName = 'bulged'
		self.labeledDirName = 'output'
		self.usedDirName = 'used'
		
	def run(self):
		try:
			self.validateHomeDir()
			
			image = self.pickImage()
			objectInImage = ObjectDetector(self.homeDir).objectIdentification(image, os.path.join(self.homeDir, self.identifiedImageDirName))
			distortedImage = Distorter(self.homeDir).distort(image, os.path.join(self.homeDir, self.bulgedDirName), objectInImage)
			stupifiedName = NameStupifier().stupify(objectInImage.name)
			distortedLabeledImage = ImageCaptioner(self.homeDir).writeText(distortedImage, os.path.join(self.homeDir, self.labeledDirName), stupifiedName)
			ImageTweeter(self.homeDir).tweetImage(distortedLabeledImage)
			self.markImageAsUsed(image)
			
			return True
			
		except Exception as e:
			self.logger.exception("Encountered an exception while attempting to run.")
			return False
		
		
		
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
