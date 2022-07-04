import unittest
from unittest.mock import Mock, MagicMock
import os.path

from TwentyTwentiesHumorBot import TwentyTwentiesHumorBot, IdentifiedObject

class BotTests(unittest.TestCase):
	
	def testRunHappyPath(self):
		filename = 'pick-a-pet-1156x650-1.jpg'
		bot = TwentyTwentiesHumorBot('test_home', tries = 1)
		bot.detector = Mock()
		idObj = IdentifiedObject('dog', [686, 636, 1632, 2515])
		bot.detector.objectIdentification = MagicMock(return_value = idObj)
		bot.distorter = Mock()
		bot.distorter.distort = MagicMock(return_value = 'distorted')
		bot.stupifier = Mock()
		bot.stupifier.stupify = MagicMock(return_value = 'stupified')
		bot.captioner = Mock()
		bot.captioner.writeText = MagicMock(return_value = 'labeled')
		bot.imageTweeter = Mock()
		bot.fileHandler = Mock()
		bot.fileHandler.identifiedDir = 'identifiedDir'
		bot.fileHandler.distortedDir = 'distortedDir'
		bot.fileHandler.labeledDir = 'labeledDir'
		bot.fileHandler.markImageAsUsed = MagicMock()
		bot.fileHandler.pickImage = MagicMock(return_value = filename)
		
		self.assertTrue(bot.run())
		
		bot.detector.objectIdentification.assert_called_once_with(filename, 'identifiedDir')
		bot.distorter.distort.assert_called_once_with(filename, 'distortedDir', idObj)
		bot.stupifier.stupify.assert_called_once_with('dog')
		bot.captioner.writeText.assert_called_once_with('distorted', 'labeledDir', 'stupified')
		bot.imageTweeter.tweetImage.assert_called_once_with('labeled')
		bot.fileHandler.markImageAsUsed.assert_called_once_with(filename)
		
	def testRunOneFailedImageThenSuccess(self):
		filename = 'pick-a-pet-1156x650-1.jpg'
		bot = TwentyTwentiesHumorBot('test_home', tries = 2)
		bot.detector = Mock()
		idObj = IdentifiedObject('dog', [686, 636, 1632, 2515])
		bot.detector.objectIdentification = MagicMock(return_value = idObj)
		bot.distorter = Mock()
		bot.distorter.distort = MagicMock(return_value = 'distorted')
		bot.stupifier = Mock()
		bot.stupifier.stupify = MagicMock(side_effect = [RuntimeError("failure on purpose"), 'stupified'])
		bot.captioner = Mock()
		bot.captioner.writeText = MagicMock(return_value = 'labeled')
		bot.imageTweeter = Mock()
		bot.fileHandler = Mock()
		bot.fileHandler.identifiedDir = 'identifiedDir'
		bot.fileHandler.distortedDir = 'distortedDir'
		bot.fileHandler.labeledDir = 'labeledDir'
		bot.fileHandler.markImageAsUsed = MagicMock()
		bot.fileHandler.markImageAsFailed = MagicMock()
		bot.fileHandler.pickImage = MagicMock(return_value = filename)
		
		self.assertTrue(bot.run())
		
		bot.detector.objectIdentification.assert_called_with(filename, 'identifiedDir')
		self.assertEquals(bot.detector.objectIdentification.call_count, 2)
		bot.distorter.distort.assert_called_with(filename, 'distortedDir', idObj)
		self.assertEquals(bot.distorter.distort.call_count, 2)
		bot.stupifier.stupify.assert_called_with('dog')
		self.assertEquals(bot.stupifier.stupify.call_count, 2)
		bot.captioner.writeText.assert_called_with('distorted', 'labeledDir', 'stupified')
		self.assertEquals(bot.captioner.writeText.call_count, 1)
		bot.imageTweeter.tweetImage.assert_called_with('labeled')
		self.assertEquals(bot.imageTweeter.tweetImage.call_count, 1)
		bot.fileHandler.markImageAsFailed.assert_called_once_with(filename)
		self.assertEquals(bot.fileHandler.markImageAsFailed.call_count, 1)
		bot.fileHandler.markImageAsUsed.assert_called_once_with(filename)
		self.assertEquals(bot.fileHandler.markImageAsUsed.call_count, 1)
		
	def testRunTwoFailed(self):
		filename = 'pick-a-pet-1156x650-1.jpg'
		bot = TwentyTwentiesHumorBot('test_home', tries = 2)
		bot.detector = Mock()
		idObj = IdentifiedObject('dog', [686, 636, 1632, 2515])
		bot.detector.objectIdentification = MagicMock(return_value = idObj)
		bot.distorter = Mock()
		bot.distorter.distort = MagicMock(return_value = 'distorted')
		bot.stupifier = Mock()
		bot.stupifier.stupify = Mock(side_effect = RuntimeError("failure on purpose"))
		bot.captioner = Mock()
		bot.captioner.writeText = MagicMock(return_value = 'labeled')
		bot.imageTweeter = Mock()
		bot.fileHandler = Mock()
		bot.fileHandler.identifiedDir = 'identifiedDir'
		bot.fileHandler.distortedDir = 'distortedDir'
		bot.fileHandler.labeledDir = 'labeledDir'
		bot.fileHandler.markImageAsUsed = MagicMock()
		bot.fileHandler.markImageAsFailed = MagicMock()
		bot.fileHandler.pickImage = MagicMock(return_value = filename)
		
		self.assertFalse(bot.run())
		
		bot.detector.objectIdentification.assert_called_with(filename, 'identifiedDir')
		bot.distorter.distort.assert_called_with(filename, 'distortedDir', idObj)
		bot.stupifier.stupify.assert_called_with('dog')
		self.assertEquals(bot.captioner.writeText.call_count, 0)
		self.assertEquals(bot.imageTweeter.tweetImage.call_count, 0)
		bot.fileHandler.markImageAsFailed.assert_called_with(filename)
		self.assertEquals(bot.fileHandler.markImageAsFailed.call_count, 2)
		self.assertEquals(bot.fileHandler.markImageAsUsed.call_count, 0)
		
	def testRunFailureAtTwitter(self):
		filename = 'pick-a-pet-1156x650-1.jpg'
		bot = TwentyTwentiesHumorBot('test_home', tries = 1)
		bot.detector = Mock()
		idObj = IdentifiedObject('dog', [686, 636, 1632, 2515])
		bot.detector.objectIdentification = MagicMock(return_value = idObj)
		bot.distorter = Mock()
		bot.distorter.distort = MagicMock(return_value = 'distorted')
		bot.stupifier = Mock()
		bot.stupifier.stupify = MagicMock(return_value = 'stupified')
		bot.captioner = Mock()
		bot.captioner.writeText = MagicMock(return_value = 'labeled')
		bot.imageTweeter = Mock()
		bot.imageTweeter.tweetImage = Mock(side_effect = RuntimeError("failure on purpose"))
		bot.fileHandler = Mock()
		bot.fileHandler.identifiedDir = 'identifiedDir'
		bot.fileHandler.distortedDir = 'distortedDir'
		bot.fileHandler.labeledDir = 'labeledDir'
		bot.fileHandler.markImageAsUsed = MagicMock()
		bot.fileHandler.markImageAsFailed = MagicMock()
		bot.fileHandler.pickImage = MagicMock(return_value = filename)
		
		self.assertFalse(bot.run())
		
		bot.detector.objectIdentification.assert_called_once_with(filename, 'identifiedDir')
		bot.distorter.distort.assert_called_once_with(filename, 'distortedDir', idObj)
		bot.stupifier.stupify.assert_called_once_with('dog')
		bot.captioner.writeText.assert_called_once_with('distorted', 'labeledDir', 'stupified')
		bot.imageTweeter.tweetImage.assert_called_once_with('labeled')
		self.assertEquals(bot.fileHandler.markImageAsFailed.call_count, 0)
		self.assertEquals(bot.fileHandler.markImageAsUsed.call_count, 0)
	
	
	
	def testRunCurationHappyPath(self):
		filename = 'Tarsier_by_mtoz.jpg'
		bot = TwentyTwentiesHumorBot('test_home', tries = 1)
		bot.detector = Mock()
		idObj = IdentifiedObject('dog', [686, 636, 1632, 2515])
		bot.detector.objectIdentification = MagicMock(return_value = idObj)
		bot.distorter = Mock()
		bot.distorter.distort = MagicMock(return_value = 'distorted')
		bot.stupifier = Mock()
		bot.stupifier.stupify = MagicMock(return_value = 'stupified')
		bot.captioner = Mock()
		bot.captioner.writeText = MagicMock(return_value = 'labeled')
		bot.imageTweeter = Mock()
		bot.fileHandler = Mock()
		bot.fileHandler.inputDirCuration = 'inputDir'
		bot.fileHandler.identifiedDirCuration = 'identifiedDir'
		bot.fileHandler.distortedDirCuration = 'distortedDir'
		bot.fileHandler.labeledDirCuration = 'labeledDir'
		bot.fileHandler.markImageAsUsed = MagicMock()
		bot.fileHandler.markImageAsFailed = MagicMock()
		bot.fileHandler.markImageAsUsedCuration = MagicMock()
		bot.fileHandler.markImageAsFailedCuration = MagicMock()
		bot.fileHandler.curationPaths = MagicMock(return_value = [filename])
		
		self.assertTrue(bot.runCuration())
		
		bot.detector.objectIdentification.assert_called_with(os.path.join('inputDir', filename), 'identifiedDir')
		bot.distorter.distort.assert_called_with(os.path.join('inputDir', filename), 'distortedDir', idObj)
		bot.stupifier.stupify.assert_called_with('dog')
		bot.captioner.writeText.assert_called_with('distorted', 'labeledDir', 'stupified')
		self.assertEquals(bot.imageTweeter.tweetImage.call_count, 0)
		self.assertEquals(bot.fileHandler.markImageAsFailed.call_count, 0)
		self.assertEquals(bot.fileHandler.markImageAsUsed.call_count, 0)
		self.assertEquals(bot.fileHandler.markImageAsFailedCuration.call_count, 0)
		self.assertEquals(bot.fileHandler.markImageAsUsedCuration.call_count, 1)
		bot.fileHandler.markImageAsUsedCuration.assert_called_once_with(os.path.join('inputDir', filename))
	
	def testRunCurationSuccessFailSuccess(self):
		filename1 = 'Tarsier_by_mtoz.jpg'
		filename2 = 'pick-a-pet-1156x650-1.jpg'
		filename3 = 'pick-a-pet-1156x650-1.jpg'
		bot = TwentyTwentiesHumorBot('test_home', tries = 1)
		bot.detector = Mock()
		idObj = IdentifiedObject('dog', [686, 636, 1632, 2515])
		bot.detector.objectIdentification = MagicMock(return_value = idObj)
		bot.distorter = Mock()
		bot.distorter.distort = MagicMock(return_value = 'distorted')
		bot.stupifier = Mock()
		bot.stupifier.stupify = MagicMock(side_effect = ['stupified', RuntimeError("failure on purpose"), 'stupified'])
		bot.captioner = Mock()
		bot.captioner.writeText = MagicMock(return_value = 'labeled')
		bot.imageTweeter = Mock()
		bot.fileHandler = Mock()
		bot.fileHandler.inputDirCuration = 'inputDir'
		bot.fileHandler.identifiedDirCuration = 'identifiedDir'
		bot.fileHandler.distortedDirCuration = 'distortedDir'
		bot.fileHandler.labeledDirCuration = 'labeledDir'
		bot.fileHandler.markImageAsUsed = MagicMock()
		bot.fileHandler.markImageAsFailed = MagicMock()
		bot.fileHandler.markImageAsUsedCuration = MagicMock()
		bot.fileHandler.markImageAsFailedCuration = MagicMock()
		bot.fileHandler.curationPaths = MagicMock(return_value = [filename1, filename2, filename3])
		
		self.assertFalse(bot.runCuration())
		
		bot.detector.objectIdentification.assert_any_call(os.path.join('inputDir', filename1), 'identifiedDir')
		bot.detector.objectIdentification.assert_any_call(os.path.join('inputDir', filename2), 'identifiedDir')
		bot.detector.objectIdentification.assert_any_call(os.path.join('inputDir', filename3), 'identifiedDir')
		self.assertEquals(bot.detector.objectIdentification.call_count, 3)
		bot.distorter.distort.assert_any_call(os.path.join('inputDir', filename1), 'distortedDir', idObj)
		bot.distorter.distort.assert_any_call(os.path.join('inputDir', filename2), 'distortedDir', idObj)
		bot.distorter.distort.assert_any_call(os.path.join('inputDir', filename3), 'distortedDir', idObj)
		self.assertEquals(bot.distorter.distort.call_count, 3)
		bot.stupifier.stupify.assert_called_with('dog')
		self.assertEquals(bot.stupifier.stupify.call_count, 3)
		bot.captioner.writeText.assert_called_with('distorted', 'labeledDir', 'stupified')
		self.assertEquals(bot.captioner.writeText.call_count, 2)
		self.assertEquals(bot.imageTweeter.tweetImage.call_count, 0)
		self.assertEquals(bot.fileHandler.markImageAsFailed.call_count, 0)
		self.assertEquals(bot.fileHandler.markImageAsUsed.call_count, 0)
		self.assertEquals(bot.fileHandler.markImageAsFailedCuration.call_count, 1)
		self.assertEquals(bot.fileHandler.markImageAsUsedCuration.call_count, 2)
		bot.fileHandler.markImageAsUsedCuration.assert_any_call(os.path.join('inputDir', filename1))
		bot.fileHandler.markImageAsFailedCuration.assert_any_call(os.path.join('inputDir', filename2))
		bot.fileHandler.markImageAsUsedCuration.assert_any_call(os.path.join('inputDir', filename3))