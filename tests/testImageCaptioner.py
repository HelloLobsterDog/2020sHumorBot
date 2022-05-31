import unittest
import tempfile
import os.path

from PIL import Image
from PIL import ImageChops

from TwentyTwentiesHumorBot import ImageCaptioner

class ImageCaptionerTests(unittest.TestCase):
	
	def setUp(self):
		self.captioner = ImageCaptioner("test_home")
		# override defaults to a known value so the test doesn't break if defaults change later
		self.captioner.textColor = (255, 255, 255)
		self.captioner.textStrokeColor = (0, 0, 0)
		self.captioner.textPadding = 20
		self.captioner.startingFontSize = 12
		self.captioner.strokeDivisor = 20
		
		self.filename = "pexels - 1170986 - EVG_Kowalievska - 'cat'.jpg"
		self.expectedFilename = "pexels - 1170986 - EVG_Kowalievska - 'cat' - captioned.jpg"
	
	def testOutputMatchesExpected(self):
		'''
		This test runs the captioner on a known image and verifies that its results don't change on the next run.
		If you even slightly change the algorithm this is likely to change (and break the test).
		This is a little more ham-fisted of a way to test this class than I'd like, but testing image manipulation code is tough
		to do at a fine grained level because it's output is an image, not some discreet data I can run asserts on.
		'''
		if not os.path.exists(os.path.join("test_home", "font")):
			raise RuntimeError("Font file not accessible. The font is not legally redistributable, so it is not available in source control, so please provide one in the directory test_home/font")
		with tempfile.TemporaryDirectory() as tempdir:
			output = self.captioner.writeText(os.path.join("test_data", self.filename), tempdir, "test")
			self.assertEqual(output, os.path.join(tempdir, self.filename))
			self.assertTrue(os.path.exists(os.path.join(tempdir, self.filename)))
			self.assertSameImage(os.path.join(tempdir, self.filename), os.path.join("test_data", self.expectedFilename))
	
	def assertSameImage(self, pathOne, pathTwo):
		image_one = Image.open(pathOne)
		image_two = Image.open(pathTwo)

		diff = ImageChops.difference(image_one, image_two)

		if diff.getbbox():
			raise AssertionError('images are different')