import unittest
import tempfile
import os.path
import random

from PIL import Image
from PIL import ImageChops

from TwentyTwentiesHumorBot import Distorter
from TwentyTwentiesHumorBot import IdentifiedObject

class DistorterTests(unittest.TestCase):
	
	def setUp(self):
		self.distorter = Distorter("test_home", random.Random(69))
		# override defaults to a known value so the test doesn't break if defaults change later
		self.distorter.bulgeAmountMin = 0.8
		self.distorter.bulgeAmountMax = 0.95
		self.distorter.bulgeRadiusMultiplier = 1.1
		self.distorter.bulgeCenteringFactor = 0.5
		
		self.filename = "pexels - 1170986 - EVG_Kowalievska - 'cat'.jpg"
		self.expectedFilename = "pexels - 1170986 - EVG_Kowalievska - 'cat' - bulged.jpg"
	
	def testOutputMatchesExpected(self):
		'''
		This test runs the distortion on a known image with known RNG state and verifies that its results don't change on the next run.
		If you even slightly tweak the algorithm this is likely to change (and break the test).
		This is a little more ham-fisted of a way to test this class than I'd like, but testing image manipulation code is tough
		to do at a fine grained level because it's output is an image, not some discreet data I can run asserts on.
		'''
		identified = IdentifiedObject("cat", [686, 636, 1632, 2515])
		with tempfile.TemporaryDirectory() as tempdir:
			output = self.distorter.bulgeImage(os.path.join("test_data", self.filename), tempdir, identified)
			self.assertTrue(os.path.exists(os.path.join(tempdir, self.filename)))
			self.assertSameImage(os.path.join(tempdir, self.filename), os.path.join("test_data", self.expectedFilename))
	
	def assertSameImage(self, pathOne, pathTwo):
		image_one = Image.open(pathOne)
		image_two = Image.open(pathTwo)

		diff = ImageChops.difference(image_one, image_two)

		if diff.getbbox():
			raise AssertionError('images are different')