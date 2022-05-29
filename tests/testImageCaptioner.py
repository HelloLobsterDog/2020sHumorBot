import unittest
import tempfile
import os.path

from PIL import Image
from PIL import ImageChops

from TwentyTwentiesHumorBot import ImageCaptioner

class ImageCaptionerTests(unittest.TestCase):
	
	def setUp(self):
		self.captioner = ImageCaptioner("test_home")
		self.filename = "pexels - 1170986 - EVG_Kowalievska - 'cat'.jpg"
		self.expectedFilename = "pexels - 1170986 - EVG_Kowalievska - 'cat' - captioned.jpg"
	
	def testOutputMatchesExpected(self):
		if not os.path.exists(os.path.join("test_home", "font")):
			raise RuntimeError("Font file not accessible. The font is not legally redistributable, so it is not available in source control, so please provide one in the directory test_home/font")
		with tempfile.TemporaryDirectory() as tempdir:
			output = self.captioner.writeText(os.path.join("test_data", self.filename), tempdir, "test")
			self.assertTrue(os.path.exists(os.path.join(tempdir, self.filename)))
			self.assertSameImage(os.path.join(tempdir, self.filename), os.path.join("test_data", self.expectedFilename))
	
	def assertSameImage(self, pathOne, pathTwo):
		image_one = Image.open(pathOne)
		image_two = Image.open(pathTwo)

		diff = ImageChops.difference(image_one, image_two)

		if diff.getbbox():
			raise AssertionError('images are different')