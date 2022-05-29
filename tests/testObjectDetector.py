import unittest
import tempfile
import os.path
from TwentyTwentiesHumorBot import ObjectDetector

class ObjectDetectorTests(unittest.TestCase):
	
	def setUp(self):
		self.detector = ObjectDetector("test_home")
		self.filename = "pexels - 1170986 - EVG_Kowalievska - 'cat'.jpg"
	
	def testOutputMatchesExpected(self):
		if not os.path.exists(os.path.join("test_home", "model")):
			raise RuntimeError("Model file not accessible. The model is not legally redistributable, so it is not available in source control, so please provide one in the directory test_home/model")
		with tempfile.TemporaryDirectory() as tempdir:
			output = self.detector.objectIdentification(os.path.join("test_data", self.filename), tempdir)
			self.assertFalse(output == None)
			self.assertTrue(os.path.exists(os.path.join(tempdir, self.filename)))
			self.assertEqual(output.name, "cat")
			self.assertEqual(output.rect, [686, 636, 1632, 2515])
		