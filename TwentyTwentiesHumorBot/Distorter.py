import logging
import os.path
import math

import cv2
import numpy

class Distorter(object):
	def __init__(self, homeDir, rand):
		self.logger = logging.getLogger('2020sHumorBot').getChild('Distorter')
		self.homeDir = homeDir
		self.rand = rand
		
		self.bulgeAmountMin = 0.85
		self.bulgeAmountMax = 0.99
		self.bulgeRadiusMultiplier = 1.4
		self.bulgeCenteringFactor = 0.4 # .5 results in all coords being moved toward the center of the object by half of their distance
	
	def distort(self, pathToImage, outputDir, objectInImage):
		return self.bulgeImage(pathToImage, outputDir, objectInImage)
		
		
		
	def bulgeImage(self, pathToImage, outputDir, objectInImage):
		# load image
		inputImage = cv2.imread(pathToImage)
		h, w, _ = inputImage.shape
		
		objectCenterX = ((objectInImage.rect[2] - objectInImage.rect[0]) / 2) + objectInImage.rect[0]
		objectCenterY = ((objectInImage.rect[3] - objectInImage.rect[1]) / 2) + objectInImage.rect[1]
		bulgeCenterX = self.rand.randrange(objectInImage.rect[0], objectInImage.rect[2])
		bulgeCenterY = self.rand.randrange(objectInImage.rect[1], objectInImage.rect[3])
		distanceCenterX = objectCenterX - bulgeCenterX
		distanceCenterY = objectCenterY - bulgeCenterY
		bulgeCenterX += distanceCenterX * self.bulgeCenteringFactor
		bulgeCenterY += distanceCenterY * self.bulgeCenteringFactor
		radius = max(objectInImage.rect[2] - objectInImage.rect[0], objectInImage.rect[3] - objectInImage.rect[1]) * self.bulgeRadiusMultiplier
		amount = self.rand.uniform(self.bulgeAmountMin, self.bulgeAmountMax)
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
		outputPath = os.path.join(outputDir, os.path.split(pathToImage)[1])
		self.logger.info("Saving bulged image to path: " + outputPath)
		cv2.imwrite(outputPath, outputImage)
		
		return outputPath