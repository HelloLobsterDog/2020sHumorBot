import unittest
from unittest.mock import Mock, MagicMock
import os.path

from TwentyTwentiesHumorBot import FileHandler

class FileHandlerTests(unittest.TestCase):
	
	def testProperties(self):
		fh = FileHandler('test_home')
		self.assertEqual(fh.identifiedDir, os.path.join('test_home', 'identified'))
		self.assertEqual(fh.distortedDir, os.path.join('test_home', 'distorted'))
		self.assertEqual(fh.labeledDir, os.path.join('test_home', 'output'))
		self.assertEqual(fh.inputDirCuration, os.path.join('test_home', 'curation', 'input'))
		self.assertEqual(fh.identifiedDirCuration, os.path.join('test_home', 'curation', 'identified'))
		self.assertEqual(fh.distortedDirCuration, os.path.join('test_home', 'curation', 'distorted'))
		self.assertEqual(fh.labeledDirCuration, os.path.join('test_home', 'curation', 'output'))
		