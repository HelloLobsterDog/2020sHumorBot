import logging
import os
import os.path

from PIL import Image, ImageFont, ImageDraw

class ImageCaptioner(object):
	def __init__(self, homeDir):
		self.logger = logging.getLogger('2020sHumorBot').getChild('ImageCaptioner')
		self.homeDir = homeDir
		
		self.textColor = (255, 255, 255)
		self.textStrokeColor = (0, 0, 0)
		self.textPadding = 20
		self.startingFontSize = 12
		self.strokeDivisor = 20
		
		self.fontFilename = None # hang onto this in between runs to save ourselves time if we're doing curation
		
	def writeText(self, imagePath, outputFolder, text):
		self.logger.info('Writing text "' + text + '" onto image from path: ' + imagePath)
		inputImage = Image.open(imagePath)
		outputImage = inputImage.copy()
		
		# get the path to the font
		fontPath = self._getFontFilename()
		self.logger.debug("loading font at path: " + fontPath)
		
		# load the font
		fontSize = self._determineFontSize(fontPath, text, outputImage)
		font = ImageFont.truetype(font=fontPath, size=fontSize)
		sizeX, sizeY = font.getsize(text)
		
		# determine draw coords
		strokeWidth = int(fontSize/self.strokeDivisor)
		drawCoords = (int((outputImage.width / 2) - (sizeX / 2)),
					  outputImage.height - sizeY - self.textPadding - strokeWidth)
		self.logger.info("Writing text with size " + str((sizeX, sizeY)) + " with stroke width " + str(strokeWidth) + " at position " + str(drawCoords))
		
		# write to the image
		drawer = ImageDraw.Draw(outputImage)
		drawer.text(drawCoords, text, font=font, fill=self.textColor, stroke_width=strokeWidth, stroke_fill=self.textStrokeColor)
		self.logger.debug("successfully written text to image")
		
		# done
		outputPath = os.path.join(outputFolder, os.path.split(imagePath)[1])
		self.logger.info("Saving output image to path: " + outputPath)
		outputImage.save(outputPath)
		outputImage.close()
		inputImage.close()
	
	def _getFontFilename(self):
		if self.fontFilename == None:
			fontDir = os.path.join(self.homeDir, "font")
			fontPathContents = os.listdir(fontDir)
			if len(fontPathContents) > 1:
				raise RuntimeError("More than one file is present in the font directory. Don't know which font to use.")
			elif len(fontPathContents) < 1:
				raise RuntimeError("No font is present in font directory.")
			fontPath = os.path.join(fontDir, fontPathContents[0])
			self.fontFilename = fontPath
			return fontPath
		else:
			return self.fontFilename
	
	def _determineFontSize(self, fontPath, text, outputImage):
		# step up the size until it's too big, and back off one, because PIL doesn't have a "write text to fill area" function.
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
		return curSize