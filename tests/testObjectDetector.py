import unittest
import tempfile
import os.path
from TwentyTwentiesHumorBot import ObjectDetector, NoDetectedObjectsError

class ObjectDetectorTests(unittest.TestCase):
	
	def setUp(self):
		self.detector = ObjectDetector("test_home", minProbability = 30)
		self.filename = "pexels - 1170986 - EVG_Kowalievska - 'cat'.jpg"
		self.overrideFilename = "1 - {override} - pexels - 1170986 - EVG_Kowalievska - 'cat'.jpg"
		self.noObjectsFilename = "pexels - 1029618 - Scott_Webb - 'building'.jpg"
	
	def testNoDetectedObjectsThrows(self):
		''' if passed an image with no identifiable objects in it, it throws an expected exception type. '''
		if not os.path.exists(os.path.join("test_home", "model")):
			raise RuntimeError("Model file not accessible. The model is not legally redistributable, so it is not available in source control, so please provide one in the directory test_home/model")
		with tempfile.TemporaryDirectory() as tempdir:
			self.assertRaises(NoDetectedObjectsError, self.detector.objectIdentification, os.path.join("test_data", self.noObjectsFilename), tempdir)
	
	def testOutputMatchesExpected(self):
		'''
		This test runs the identification on a known image and verifies that its results don't change from an expected case.
		If you change models this is likely to change (and break the test).
		This is a little more ham-fisted of a way to test this class than I'd like, but testing AI stuff is tough.
		'''
		if not os.path.exists(os.path.join("test_home", "model")):
			raise RuntimeError("Model file not accessible. The model is not legally redistributable, so it is not available in source control, so please provide one in the directory test_home/model")
		with tempfile.TemporaryDirectory() as tempdir:
			output = self.detector.objectIdentification(os.path.join("test_data", self.filename), tempdir)
			self.assertFalse(output == None)
			self.assertTrue(os.path.exists(os.path.join(tempdir, self.filename)))
			self.assertEqual(output.name, "cat")
			self.assertEqual(output.rect, [686, 636, 1632, 2515])
		
	
	def testIDOverride(self):
		if not os.path.exists(os.path.join("test_home", "model")):
			raise RuntimeError("Model file not accessible. The model is not legally redistributable, so it is not available in source control, so please provide one in the directory test_home/model")
		with tempfile.TemporaryDirectory() as tempdir:
			output = self.detector.objectIdentification(os.path.join("test_data", self.overrideFilename), tempdir)
			self.assertFalse(output == None)
			self.assertEqual(output.name, "override")
		