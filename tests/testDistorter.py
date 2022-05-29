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
		self.filename = "pexels - 1170986 - EVG_Kowalievska - 'cat'.jpg"
		self.expectedFilename = "pexels - 1170986 - EVG_Kowalievska - 'cat' - bulged.jpg"
	
	def testOutputMatchesExpected(self):
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