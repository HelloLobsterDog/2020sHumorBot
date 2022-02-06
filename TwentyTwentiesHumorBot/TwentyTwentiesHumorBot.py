import logging
import os
import os.path
import random
import math

from imageai.Detection import ObjectDetection
from EasyTweeter import EasyTweeter
from PIL import Image, ImageFont, ImageDraw
import numpy
import cv2

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
		self.bulgedDirName = 'bulged'
		self.labeledDirName = 'output'
		self.usedDirName = 'used'
		# object detection
		self.minProbability = 10
		# image bulging
		self.bulgeAmountMin = 0.8
		self.bulgeAmountMax = 0.95
		self.bulgeRadiusMultiplier = 1.1
		self.bulgeCenteringFactor = 0.5 # .5 results in all coords being moved toward the center of the object by half of their distance
		# text writing
		self.textColor = (255, 255, 255)
		self.textStrokeColor = (0, 0, 0)
		self.textPadding = 20
		self.startingFontSize = 12
		self.strokeDivisor = 20
		# twitter
		self.twitterInteractionCheckInterval = 5
		
	def run(self):
		try:
			self.validateHomeDir()
			
			image = self.pickImage()
			objectInImage = self.objectIdentification(image)
			bulgedImage = self.bulgeImage(image, objectInImage)
			stupifiedName = self.stupifyName(objectInImage)
			bulgedLabeledImage = self.writeText(bulgedImage, stupifiedName)
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
		
	def bulgeImage(self, pathToImage, objectInImage):
		# load image
		inputImage = cv2.imread(pathToImage)
		h, w, _ = inputImage.shape
		
		objectCenterX = ((objectInImage.rect[2] - objectInImage.rect[0]) / 2) + objectInImage.rect[0]
		objectCenterY = ((objectInImage.rect[3] - objectInImage.rect[1]) / 2) + objectInImage.rect[1]
		bulgeCenterX = random.randrange(objectInImage.rect[0], objectInImage.rect[2])
		bulgeCenterY = random.randrange(objectInImage.rect[1], objectInImage.rect[3])
		distanceCenterX = objectCenterX - bulgeCenterX
		distanceCenterY = objectCenterY - bulgeCenterY
		bulgeCenterX += distanceCenterX * self.bulgeCenteringFactor
		bulgeCenterY += distanceCenterY * self.bulgeCenteringFactor
		radius = max(objectInImage.rect[2] - objectInImage.rect[0], objectInImage.rect[3] - objectInImage.rect[1]) * self.bulgeRadiusMultiplier
		amount = random.uniform(self.bulgeAmountMin, self.bulgeAmountMax)
		scaleY = 1
		scaleX = 1
		self.logger.info("bulging image centered at (" + str(bulgeCenterX) + ", " + str(bulgeCenterY) + ") (random position moved toward real center by " + str(distanceCenterX * self.bulgeCenteringFactor) + ", " + str(distanceCenterY * self.bulgeCenteringFactor) + ") with radius " + str(radius) + " by amount " + str(amount))
		
		# setup numpy maps
		flexX = numpy.zeros((h, w), numpy.float32)
		flexY = numpy.zeros((h, w), numpy.float32)
		
		# fill the map with distoration formula
		self.logger.debug('filling distoration arrays...')
		for y in range(h):
			deltaY = scaleY * (y - bulgeCenterY)
			for x in range(w):
				# determine if pixel is within an ellipse
				deltaX = scaleX * (x - bulgeCenterX)
				distance = deltaX * deltaX + deltaY * deltaY
				if distance >= radius * radius:
					flexX[y, x] = x
					flexY[y, x] = y
				else:
					factor = 1.0
					if distance > 0.0:
						factor = math.pow(math.sin(math.pi * math.sqrt(distance) / radius / 2), amount)
					flexX[y, x] = factor * deltaX / scaleX + bulgeCenterX
					flexY[y, x] = factor * deltaY / scaleY + bulgeCenterY
		
		# do the actual remap in the image with the maps
		self.logger.debug("remapping...")
		outputImage = cv2.remap(inputImage, flexX, flexY, cv2.INTER_LINEAR)
		self.logger.debug("successfully remapped.")
		
		# save it back to a file
		outputPath = os.path.join(self.homeDir, self.bulgedDirName, os.path.split(pathToImage)[1])
		self.logger.info("Saving bulged image to path: " + outputPath)
		cv2.imwrite(outputPath, outputImage)
		
		return outputPath
		
	def stupifyName(self, objectInImage):
		return objectInImage.name # TODO
		
	def writeText(self, imagePath, text):
		self.logger.info('Writing text "' + text + '" onto image from path: ' + imagePath)
		inputImage = Image.open(imagePath)
		outputImage = inputImage.copy()
		
		# get the path to the font
		fontDir = os.path.join(self.homeDir, "font")
		fontPathContents = os.listdir(fontDir)
		if len(fontPathContents) > 1:
			raise RuntimeError("More than one file is present in the font directory. Don't know which font to use.")
		elif len(fontPathContents) < 1:
			raise RuntimeError("No font is present in font directory.")
		fontPath = os.path.join(fontDir, fontPathContents[0])
		self.logger.debug("loading font at path: " + fontPath)
		
		# Load the font at the right size (step up the size until it's too big, and back off one), because PIL doesn't have a "write text to fill area" function.
		# This is very slow and inefficient, but whatever, object identification is orders of magnitude slower than this will ever be.
		maxX = outputImage.width - self.textPadding * 2
		maxY = int(outputImage.height/4)
		self.logger.debug("Allowing text to take up a maximum space of size " + str((maxX, maxY)))
		curSize = self.startingFontSize
		font = ImageFont.truetype(font=fontPath, size=curSize)
		sizeX, sizeY = font.getsize(text)
		while sizeX <= maxX and sizeY <= maxY:
			curSize += 1
			font = ImageFont.truetype(font=fontPath, size=curSize)
			sizeX, sizeY = font.getsize(text)
		# back off one
		curSize -= 1
		self.logger.info("Determined that font size " + str(curSize) + " will fit in the allowed area after " + str(curSize - self.startingFontSize + 2) + " iterations.")
		font = ImageFont.truetype(font=fontPath, size=curSize)
		sizeX, sizeY = font.getsize(text)
		
		# determine draw coords
		strokeWidth = int(curSize/self.strokeDivisor)
		drawCoords = (int((outputImage.width / 2) - (sizeX / 2)),
					  outputImage.height - sizeY - self.textPadding - strokeWidth)
		self.logger.info("Writing text with size " + str((sizeX, sizeY)) + " with stroke width " + str(strokeWidth) + " at position " + str(drawCoords))
		
		# write to the image
		drawer = ImageDraw.Draw(outputImage)
		drawer.text(drawCoords, text, font=font, fill=self.textColor, stroke_width=strokeWidth, stroke_fill=self.textStrokeColor)
		self.logger.debug("successfully written text to image")
		
		# done
		outputPath = os.path.join(self.homeDir, self.labeledDirName, os.path.split(imagePath)[1])
		self.logger.info("Saving output image to path: " + outputPath)
		outputImage.save(outputPath)
		outputImage.close()
		inputImage.close()
		
	def tweetImage(self, imagePath):
		self.logger.debug("tweeting image...")
		bot = BotIntegratedEasyTweeter(self.homeDir, logger = self.logger.getChild("easytweeter"))
		try:
			bot.tweetImage(imagePath)
			bot.checkForUpdates(self.twitterInteractionCheckInterval, directMessages = False)
			
		except Exception as e:
			bot.logger.exception('Exception caused twitter bot to fail.')
			raise e
				
		bot.logger.info("Bot completed successfully.\n")
		
	def markImageAsUsed(self, path):
		pathToMoveTo = os.path.join(self.homeDir, self.usedDirName, os.path.basename(path))
		os.rename(path, pathToMoveTo)
		self.logger.info("image %s moved to used folder: %s", path, pathToMoveTo)
