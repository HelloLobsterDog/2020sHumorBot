import logging
import os
import os.path
import random

from imageai.Detection import ObjectDetection

class IdentifiedObject(object):
	def __init__(self, name, rect):
		self.name = name
		self.rect = rect

class TwentyTwentiesHumorBot(object):
	def __init__(self, homeDir):
		self.homeDir = homeDir
		self.logger = logging.getLogger('2020sHumorBot')
		
		self.inputImageDirName = 'input'
		self.identifiedImageDirName = 'identified'
		self.minProbability = 50
		
	def run(self):
		try:
			self.validateHomeDir()
			
			image = self.pickImage()
			objectInImage = self.objectIdentification(image)
			stupifiedName = self.stupifyName(objectInImage)
			bulgedImage = self.bulgeImage(image, objectInImage)
			bulgedLabeledImage = self.writeText(bulgedImage, stupifiedName)
			self.saveImageToFile(bulgedLabeledImage)
			self.tweetImage(bulgedLabeledImage)
			self.markImageAsUsed(image)
			
			return True
			
		except Exception as e:
			self.logger.exception("Encountered an exception while attempting to run.")
			return False
		
		
		
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
		
		modelPath = os.path.join(self.homeDir, "model")
		modelPathContents = os.listdir(modelPath)
		if len(modelPathContents) > 1:
			raise RuntimeError("More than one file is present in the model directory. Don't know which model to use.")
		elif len(modelPathContents) < 1:
			raise RuntimeError("No model is present in model directory.")
		detector.setModelPath(modelPathContents[0])
		
		self.logger.info("Loading model from %s", modelPathContents[0])
		detector.loadModel()
		self.logger.debug("Successfully loaded model.")
		
		self.logger.info("Detecting objects in image...")
		detections = detector.detectObjectsFromImage(input_image=pathToImage, output_image_path=os.path.join(self.homeDir, self.identifiedImageDirName, os.path.basename(pathToImage)), minimum_percentage_probability = self.minProbability)
		self.logger.info("Successfully detected %s objects.", str(len(detections)))
		
		things = []
		for thing in detections:
			self.logger.info(eachObject["name"] + " : " + eachObject["percentage_probability"] + " : " + str(eachObject["box_points"]))
			things.append(IdentifiedObject(eachObject["name"], eachObject["box_points"])
		things.sort(key=lambda x: self._areaOfBox(x), reverse=True)
		
		return things[0]
		
	def _areaOfBox(self, boxPoints):
		return (boxPoints[2] - boxPoints[0]) * (boxPoints[3] - boxPoints[1])
		
	def stupifyName(self, objectInImage):
		pass # TODO
		
	def bulgeImage(self, pathToImage, objectInImage):
		pass # TODO
		
	def writeText(self, image, text):
		pass # TODO
		
	def saveImageToFile(self, image):
		pass # TODO
		
	def tweetImage(self, image):
		pass # TODO
		
	def markImageAsUsed(self, path):
		pass # TODO
