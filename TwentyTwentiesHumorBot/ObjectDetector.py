import logging
import os
import os.path

from imageai.Detection import ObjectDetection

class IdentifiedObject(object):
	def __init__(self, name, rect):
		self.name = name
		self.rect = rect # tuple of (x1, y1, x2, y2)

class ObjectDetector(object):
	def __init__(self, homeDir, minProbability = 10):
		self.logger = logging.getLogger('2020sHumorBot').getChild('ObjectDetector')
		
		self.homeDir = homeDir
		self.minProbability = minProbability
	
	
	def objectIdentification(self, pathToImage, outputFolder):
		detector = ObjectDetection()
		self._loadModel(detector)
		
		self.logger.info("Detecting objects in image...")
		detections = detector.detectObjectsFromImage(input_image=pathToImage, output_image_path=os.path.join(outputFolder, os.path.basename(pathToImage)), minimum_percentage_probability = self.minProbability)
		self.logger.info("Successfully detected %s objects.", str(len(detections)))
		
		things = []
		for thing in detections:
			self.logger.info("object detected: " + thing["name"] + " : " + str(thing["percentage_probability"]) + " : " + str(thing["box_points"]))
			things.append(IdentifiedObject(thing["name"], thing["box_points"]))
		things.sort(key=lambda x: self._areaOfBox(x), reverse=True)
		
		return things[0]
		
	def _loadModel(self, detector):
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
		
		
	def _areaOfBox(self, obj):
		return (obj.rect[2] - obj.rect[0]) * (obj.rect[3] - obj.rect[1])