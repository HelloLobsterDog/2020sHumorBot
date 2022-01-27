import logging
import os
import os.path
import random

from imageai.Detection import ObjectDetection
from EasyTweeter import EasyTweeter

class IdentifiedObject(object):
	def __init__(self, name, rect):
		self.name = name
		self.rect = rect # tuple of (x1, y1, x2, y2)
		
class BotIntegratedEasyTweeter(EasyTweeter):
	def getStateDirectory(self):
		return os.path.join(self.configurationDirectory, 'EasyTweeterState')

class TwentyTwentiesHumorBot(object):
	def __init__(self, homeDir):
		self.homeDir = homeDir
		self.logger = logging.getLogger('2020sHumorBot')
		
		self.inputImageDirName = 'input'
		self.identifiedImageDirName = 'identified'
		self.usedDirName = 'used'
		self.minProbability = 50
		self.twitterInteractionCheckInterval = 5
		
	def run(self):
		try:
			self.validateHomeDir()
			
			image = self.pickImage()
			objectInImage = self.objectIdentification(image)
			bulgedImage = self.bulgeImage(image, objectInImage)
			stupifiedName = self.stupifyName(objectInImage)
			bulgedLabeledImage = self.writeText(bulgedImage, stupifiedName)
			self.saveImageToFile(bulgedLabeledImage)
			self.tweetImage(bulgedLabeledImage)
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
		
	def objectIdentification(self, pathToImage):
		detector = ObjectDetection()
		detector.setModelTypeAsRetinaNet()
		
		modelDir = os.path.join(self.homeDir, "model")
		modelPathContents = os.listdir(modelDir)
		if len(modelPathContents) > 1:
			raise RuntimeError("More than one file is present in the model directory. Don't know which model to use.")
		elif len(modelPathContents) < 1:
			raise RuntimeError("No model is present in model directory.")
		modelPath = os.path.join(modelDir, modelPathContents[0])
		detector.setModelPath(modelPath)
		
		self.logger.info("Loading model from %s", modelPath)
		detector.loadModel()
		self.logger.debug("Successfully loaded model.")
		
		self.logger.info("Detecting objects in image...")
		detections = detector.detectObjectsFromImage(input_image=pathToImage, output_image_path=os.path.join(self.homeDir, self.identifiedImageDirName, os.path.basename(pathToImage)), minimum_percentage_probability = self.minProbability)
		self.logger.info("Successfully detected %s objects.", str(len(detections)))
		
		things = []
		for thing in detections:
			self.logger.info("object detected: " + thing["name"] + " : " + str(thing["percentage_probability"]) + " : " + str(thing["box_points"]))
			things.append(IdentifiedObject(thing["name"], thing["box_points"]))
		things.sort(key=lambda x: self._areaOfBox(x), reverse=True)
		
		return things[0]
		
	def _areaOfBox(self, obj):
		return (obj.rect[2] - obj.rect[0]) * (obj.rect[3] - obj.rect[1])
		
	def stupifyName(self, objectInImage):
		pass # TODO
		
	def bulgeImage(self, pathToImage, objectInImage):
		pass # TODO
		
	def writeText(self, image, text):
		pass # TODO
		
	def saveImageToFile(self, image):
		pass # TODO
		
	def tweetImage(self, image):
		self.logger.debug("tweeting image...")
		bot = BotIntegratedEasyTweeter(self.homeDir, logger = self.logger.getChild("easytweeter"))
		try:
			bot.tweetImage(image)
			bot.checkForUpdates(self.twitterInteractionCheckInterval, directMessages = False)
			
		except Exception as e:
			bot.logger.exception('Exception caused twitter bot to fail.')
			raise e
				
		bot.logger.info("Bot completed successfully.\n")
		
	def markImageAsUsed(self, path):
		pathToMoveTo = os.path.join(self.homeDir, self.usedDirName, os.path.basename(path))
		os.rename(path, pathToMoveTo)
		self.logger.info("image %s moved to used folder: %s", path, pathToMoveTo)
