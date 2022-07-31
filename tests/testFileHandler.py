import unittest
from unittest.mock import Mock, MagicMock
import os.path
import shutil
import tempfile
import random

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
		
	def testPickImageHappyPath(self):
		filename = "pexels - 1170986 - EVG_Kowalievska - 'cat'.jpg"
		with tempfile.TemporaryDirectory() as tempdir:
			# setup
			os.makedirs(os.path.join(tempdir, 'test_home', 'input'))
			shutil.copyfile(os.path.join('test_data', filename), os.path.join(tempdir, 'test_home', 'input', filename))
			
			fh = FileHandler(os.path.join(tempdir, 'test_home'))
			
			# execute
			picked = fh.pickImage()
			
			# validate
			self.assertEqual(picked, os.path.join(tempdir, 'test_home', 'input', filename))
			self.assertTrue(os.path.exists(os.path.join(tempdir, 'test_home', 'input', filename)))
			self.assertTrue(os.path.exists(fh.identifiedDir))
			self.assertTrue(os.path.exists(fh.distortedDir))
			self.assertTrue(os.path.exists(fh.labeledDir))
	
	def testPickImageOutOfInput(self):
		filename = "pexels - 1170986 - EVG_Kowalievska - 'cat'.jpg"
		with tempfile.TemporaryDirectory() as tempdir:
			# setup
			os.makedirs(os.path.join(tempdir, 'test_home', 'input'))
			os.makedirs(os.path.join(tempdir, 'test_home', 'used'))
			shutil.copyfile(os.path.join('test_data', filename), os.path.join(tempdir, 'test_home', 'used', filename))
			
			fh = FileHandler(os.path.join(tempdir, 'test_home'))
			
			# execute
			picked = fh.pickImage()
			
			# validate
			self.assertEqual(picked, os.path.join(tempdir, 'test_home', 'input', filename))
			self.assertTrue(os.path.exists(os.path.join(tempdir, 'test_home', 'input', filename)))
			self.assertFalse(os.path.exists(os.path.join(tempdir, 'test_home', 'test_home', 'used', filename)))
			self.assertTrue(os.path.exists(fh.identifiedDir))
			self.assertTrue(os.path.exists(fh.distortedDir))
			self.assertTrue(os.path.exists(fh.labeledDir))
		
	def testPickImageOutOfInputAndUsed(self):
		with tempfile.TemporaryDirectory() as tempdir:
			# setup
			os.makedirs(os.path.join(tempdir, 'test_home', 'input'))
			os.makedirs(os.path.join(tempdir, 'test_home', 'used'))
			
			fh = FileHandler(os.path.join(tempdir, 'test_home'))
			
			# execute
			self.assertRaises(RuntimeError, fh.pickImage)
			
			# validate
			self.assertFalse(os.listdir(os.path.join(tempdir, 'test_home', 'input')))
			self.assertFalse(os.listdir(os.path.join(tempdir, 'test_home', 'used')))
			self.assertFalse(os.path.exists(fh.identifiedDir))
			self.assertFalse(os.path.exists(fh.distortedDir))
			self.assertFalse(os.path.exists(fh.labeledDir))
	
	def testMarkImageAsFailed(self):
		filename = "pexels - 1170986 - EVG_Kowalievska - 'cat'.jpg"
		with tempfile.TemporaryDirectory() as tempdir:
			# setup
			os.makedirs(os.path.join(tempdir, 'test_home', 'input'))
			shutil.copyfile(os.path.join('test_data', filename), os.path.join(tempdir, 'test_home', 'input', filename))
			
			fh = FileHandler(os.path.join(tempdir, 'test_home'))
			
			# execute
			fh.markImageAsFailed(os.path.join(tempdir, 'test_home', 'input', filename))
			
			# validate
			self.assertFalse(os.path.exists(os.path.join(tempdir, 'test_home', 'input', filename)))
			self.assertTrue(os.path.exists(os.path.join(tempdir, 'test_home', 'failed', filename)))
	
	def testMarkImageAsFailedAlreadyPresent(self):
		random.seed(42069)
		filename = "pexels - 1170986 - EVG_Kowalievska - 'cat'.jpg"
		with tempfile.TemporaryDirectory() as tempdir:
			# setup
			os.makedirs(os.path.join(tempdir, 'test_home', 'input'))
			os.makedirs(os.path.join(tempdir, 'test_home', 'failed'))
			shutil.copyfile(os.path.join('test_data', filename), os.path.join(tempdir, 'test_home', 'input', filename))
			shutil.copyfile(os.path.join('test_data', filename), os.path.join(tempdir, 'test_home', 'failed', filename))
			
			fh = FileHandler(os.path.join(tempdir, 'test_home'))
			
			# execute
			fh.markImageAsFailed(os.path.join(tempdir, 'test_home', 'input', filename))
			
			# validate
			self.assertFalse(os.path.exists(os.path.join(tempdir, 'test_home', 'input', filename)))
			self.assertTrue(os.path.exists(os.path.join(tempdir, 'test_home', 'failed', filename)))
			self.assertTrue(os.path.exists(os.path.join(tempdir, 'test_home', 'failed', filename + ".860")))
		
	def testMarkImageAsUsedNoNumber(self):
		filename = "pexels - 1170986 - EVG_Kowalievska - 'cat'.jpg"
		expectedFilename = "1 - pexels - 1170986 - EVG_Kowalievska - 'cat'.jpg"
		with tempfile.TemporaryDirectory() as tempdir:
			# setup
			os.makedirs(os.path.join(tempdir, 'test_home', 'input'))
			shutil.copyfile(os.path.join('test_data', filename), os.path.join(tempdir, 'test_home', 'input', filename))
			
			fh = FileHandler(os.path.join(tempdir, 'test_home'))
			
			# execute
			fh.markImageAsUsed(os.path.join(tempdir, 'test_home', 'input', filename))
			
			# validate
			self.assertFalse(os.path.exists(os.path.join(tempdir, 'test_home', 'input', filename)))
			self.assertTrue(os.path.exists(os.path.join(tempdir, 'test_home', 'used', expectedFilename)))
		
	def testMarkImageAsUsedNoNumberNoSpaces(self):
		beginningFilename = "pexels - 1170986 - EVG_Kowalievska - 'cat'.jpg"
		filename = '1thisFilenameHasNoSpacesInItWhichMessesUpTheAlgorithm.jpg'
		expectedFilename = "1 - 1thisFilenameHasNoSpacesInItWhichMessesUpTheAlgorithm.jpg"
		with tempfile.TemporaryDirectory() as tempdir:
			# setup
			os.makedirs(os.path.join(tempdir, 'test_home', 'input'))
			shutil.copyfile(os.path.join('test_data', beginningFilename), os.path.join(tempdir, 'test_home', 'input', filename))
			
			fh = FileHandler(os.path.join(tempdir, 'test_home'))
			
			# execute
			fh.markImageAsUsed(os.path.join(tempdir, 'test_home', 'input', filename))
			
			# validate
			self.assertFalse(os.path.exists(os.path.join(tempdir, 'test_home', 'input', filename)))
			self.assertTrue(os.path.exists(os.path.join(tempdir, 'test_home', 'used', expectedFilename)))
		
	def testMarkImageAsUsedYesNumber(self):
		unnumberedFilename = "pexels - 1170986 - EVG_Kowalievska - 'cat'.jpg"
		filename = "1 - pexels - 1170986 - EVG_Kowalievska - 'cat'.jpg"
		expectedFilename = "2 - pexels - 1170986 - EVG_Kowalievska - 'cat'.jpg"
		with tempfile.TemporaryDirectory() as tempdir:
			# setup
			os.makedirs(os.path.join(tempdir, 'test_home', 'input'))
			shutil.copyfile(os.path.join('test_data', unnumberedFilename), os.path.join(tempdir, 'test_home', 'input', filename))
			
			fh = FileHandler(os.path.join(tempdir, 'test_home'))
			
			# execute
			fh.markImageAsUsed(os.path.join(tempdir, 'test_home', 'input', filename))
			
			# validate
			self.assertFalse(os.path.exists(os.path.join(tempdir, 'test_home', 'input', filename)))
			self.assertTrue(os.path.exists(os.path.join(tempdir, 'test_home', 'used', expectedFilename)))
	
	
	
	def testCurationPaths(self):
		filename = "pexels - 1170986 - EVG_Kowalievska - 'cat'.jpg"
		second = "same file but again.jpg"
		with tempfile.TemporaryDirectory() as tempdir:
			# setup
			os.makedirs(os.path.join(tempdir, 'test_home', 'curation', 'input'))
			shutil.copyfile(os.path.join('test_data', filename), os.path.join(tempdir, 'test_home', 'curation', 'input', filename))
			self.assertTrue(os.path.exists(os.path.join(tempdir, 'test_home', 'curation', 'input', filename)))
			shutil.copyfile(os.path.join('test_data', filename), os.path.join(tempdir, 'test_home', 'curation', 'input', second))
			self.assertTrue(os.path.exists(os.path.join(tempdir, 'test_home', 'curation', 'input', second)))
			
			fh = FileHandler(os.path.join(tempdir, 'test_home'))
			
			# execute
			paths = []
			for f in fh.curationPaths():
				paths.append(f)
			
			# validate
			self.assertEqual(2, len(paths))
			self.assertTrue(filename in paths)
			self.assertTrue(second in paths)
			self.assertTrue(os.path.exists(fh.identifiedDirCuration))
			self.assertTrue(os.path.exists(fh.distortedDirCuration))
			self.assertTrue(os.path.exists(fh.labeledDirCuration))
		
	def testMarkImageAsFailedCuration(self):
		filename = "pexels - 1170986 - EVG_Kowalievska - 'cat'.jpg"
		with tempfile.TemporaryDirectory() as tempdir:
			# setup
			os.makedirs(os.path.join(tempdir, 'test_home', 'curation', 'input'))
			shutil.copyfile(os.path.join('test_data', filename), os.path.join(tempdir, 'test_home', 'curation', 'input', filename))
			
			fh = FileHandler(os.path.join(tempdir, 'test_home'))
			
			# execute
			fh.markImageAsFailedCuration(os.path.join(tempdir, 'test_home', 'curation', 'input', filename))
			
			# validate
			self.assertFalse(os.path.exists(os.path.join(tempdir, 'test_home', 'curation', 'input', filename)))
			self.assertTrue(os.path.exists(os.path.join(tempdir, 'test_home', 'curation', 'failed', filename)))
		
	def testMarkImageAsFailedCurationAlreadyPresent(self):
		random.seed(42069)
		filename = "pexels - 1170986 - EVG_Kowalievska - 'cat'.jpg"
		with tempfile.TemporaryDirectory() as tempdir:
			# setup
			os.makedirs(os.path.join(tempdir, 'test_home', 'curation', 'input'))
			os.makedirs(os.path.join(tempdir, 'test_home', 'curation', 'failed'))
			shutil.copyfile(os.path.join('test_data', filename), os.path.join(tempdir, 'test_home', 'curation', 'failed', filename))
			shutil.copyfile(os.path.join('test_data', filename), os.path.join(tempdir, 'test_home', 'curation', 'input', filename))
			
			fh = FileHandler(os.path.join(tempdir, 'test_home'))
			
			# execute
			fh.markImageAsFailedCuration(os.path.join(tempdir, 'test_home', 'curation', 'input', filename))
			
			# validate
			self.assertFalse(os.path.exists(os.path.join(tempdir, 'test_home', 'curation', 'input', filename)))
			self.assertTrue(os.path.exists(os.path.join(tempdir, 'test_home', 'curation', 'failed', filename)))
			self.assertTrue(os.path.exists(os.path.join(tempdir, 'test_home', 'curation', 'failed', filename + ".860")))
		
	def testMarkImageAsUSedCuration(self):
		filename = "pexels - 1170986 - EVG_Kowalievska - 'cat'.jpg"
		with tempfile.TemporaryDirectory() as tempdir:
			# setup
			os.makedirs(os.path.join(tempdir, 'test_home', 'curation', 'input'))
			shutil.copyfile(os.path.join('test_data', filename), os.path.join(tempdir, 'test_home', 'curation', 'input', filename))
			
			fh = FileHandler(os.path.join(tempdir, 'test_home'))
			
			# execute
			fh.markImageAsUsedCuration(os.path.join(tempdir, 'test_home', 'curation', 'input', filename))
			
			# validate
			self.assertFalse(os.path.exists(os.path.join(tempdir, 'test_home', 'curation', 'input', filename)))
			self.assertTrue(os.path.exists(os.path.join(tempdir, 'test_home', 'curation', 'successful', filename)))
		