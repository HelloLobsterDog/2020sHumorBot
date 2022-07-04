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
		
		self.assertTrue(bot.run())
		
		bot.detector.objectIdentification.assert_called_once_with(os.path.join('test_home', 'input', filename), os.path.join('test_home', 'identified'))
		bot.distorter.distort.assert_called_once_with(os.path.join('test_home', 'input', filename), os.path.join('test_home', 'bulged'), idObj)
		bot.stupifier.stupify.assert_called_once_with('dog')
		bot.captioner.writeText.assert_called_once_with('distorted', os.path.join('test_home', 'output'), 'stupified')
		bot.imageTweeter.tweetImage.assert_called_once_with('labeled')
		
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
		
		self.assertTrue(bot.run())
		
		bot.detector.objectIdentification.assert_called_with(os.path.join('test_home', 'input', filename), os.path.join('test_home', 'identified'))
		self.assertEquals(bot.detector.objectIdentification.call_count, 2)
		bot.distorter.distort.assert_called_with(os.path.join('test_home', 'input', filename), os.path.join('test_home', 'bulged'), idObj)
		self.assertEquals(bot.distorter.distort.call_count, 2)
		bot.stupifier.stupify.assert_called_with('dog')
		self.assertEquals(bot.stupifier.stupify.call_count, 2)
		bot.captioner.writeText.assert_called_with('distorted', os.path.join('test_home', 'output'), 'stupified')
		self.assertEquals(bot.captioner.writeText.call_count, 1)
		bot.imageTweeter.tweetImage.assert_called_with('labeled')
		self.assertEquals(bot.imageTweeter.tweetImage.call_count, 1)
		
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
		
		self.assertFalse(bot.run())
		
		bot.detector.objectIdentification.assert_called_with(os.path.join('test_home', 'input', filename), os.path.join('test_home', 'identified'))
		bot.distorter.distort.assert_called_with(os.path.join('test_home', 'input', filename), os.path.join('test_home', 'bulged'), idObj)
		bot.stupifier.stupify.assert_called_with('dog')
		self.assertEquals(bot.captioner.writeText.call_count, 0)
		self.assertEquals(bot.imageTweeter.tweetImage.call_count, 0)
		
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
		
		self.assertFalse(bot.run())
		
		bot.detector.objectIdentification.assert_called_once_with(os.path.join('test_home', 'input', filename), os.path.join('test_home', 'identified'))
		bot.distorter.distort.assert_called_once_with(os.path.join('test_home', 'input', filename), os.path.join('test_home', 'bulged'), idObj)
		bot.stupifier.stupify.assert_called_once_with('dog')
		bot.captioner.writeText.assert_called_once_with('distorted', os.path.join('test_home', 'output'), 'stupified')
		bot.imageTweeter.tweetImage.assert_called_once_with('labeled')
	
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
		
		self.assertTrue(bot.runCuration())
		
		bot.detector.objectIdentification.assert_called_with(os.path.join('test_home', 'curation', 'input', filename), os.path.join('test_home', 'curation', 'identified'))
		bot.distorter.distort.assert_called_with(os.path.join('test_home', 'curation', 'input', filename), os.path.join('test_home', 'curation', 'bulged'), idObj)
		bot.stupifier.stupify.assert_called_with('dog')
		bot.captioner.writeText.assert_called_with('distorted', os.path.join('test_home', 'curation', 'output'), 'stupified')
		self.assertEquals(bot.imageTweeter.tweetImage.call_count, 0)
	
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
		
		self.assertFalse(bot.runCuration())
		
		bot.detector.objectIdentification.assert_any_call(os.path.join('test_home', 'curation', 'input', filename1), os.path.join('test_home', 'curation', 'identified'))
		bot.detector.objectIdentification.assert_any_call(os.path.join('test_home', 'curation', 'input', filename2), os.path.join('test_home', 'curation', 'identified'))
		bot.detector.objectIdentification.assert_any_call(os.path.join('test_home', 'curation', 'input', filename3), os.path.join('test_home', 'curation', 'identified'))
		self.assertEquals(bot.detector.objectIdentification.call_count, 3)
		bot.distorter.distort.assert_any_call(os.path.join('test_home', 'curation', 'input', filename1), os.path.join('test_home', 'curation', 'bulged'), idObj)
		bot.distorter.distort.assert_any_call(os.path.join('test_home', 'curation', 'input', filename2), os.path.join('test_home', 'curation', 'bulged'), idObj)
		bot.distorter.distort.assert_any_call(os.path.join('test_home', 'curation', 'input', filename3), os.path.join('test_home', 'curation', 'bulged'), idObj)
		self.assertEquals(bot.distorter.distort.call_count, 3)
		bot.stupifier.stupify.assert_called_with('dog')
		self.assertEquals(bot.stupifier.stupify.call_count, 3)
		bot.captioner.writeText.assert_called_with('distorted', os.path.join('test_home', 'curation', 'output'), 'stupified')
		self.assertEquals(bot.captioner.writeText.call_count, 2)
		self.assertEquals(bot.imageTweeter.tweetImage.call_count, 0)