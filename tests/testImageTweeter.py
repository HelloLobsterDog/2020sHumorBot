import unittest
from unittest.mock import Mock

from TwentyTwentiesHumorBot import ImageTweeter

mockEasyTweeter = Mock()
def asdf(_, path, logger):
	return mockEasyTweeter

class ImageTweeterTests(unittest.TestCase):
	
	def testMethodsCalledAsExpected(self):
		''' this test isn't actually testing a whole lot. Pretty Much just that we call the library as expected. '''
		ImageTweeter.botClass = asdf
		self.tweeter = ImageTweeter("asdf", twitterInteractionCheckInterval = 6)
		self.tweeter.tweetImage("pretend this is a real file path")
		
		mockEasyTweeter.tweetImage.assert_called_with("pretend this is a real file path")
		mockEasyTweeter.checkForUpdates.assert_called_with(6, directMessages = False)