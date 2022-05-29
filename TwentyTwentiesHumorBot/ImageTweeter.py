import logging

from EasyTweeter import EasyTweeter
		
class BotIntegratedEasyTweeter(EasyTweeter):
	def getStateDirectory(self):
		return os.path.join(self.configurationDirectory, 'EasyTweeterState')
		
	
class ImageTweeter(object):
	botClass = BotIntegratedEasyTweeter # makes the unit test easier to write
	def __init__(self, homeDir, twitterInteractionCheckInterval = 5):
		self.logger = logging.getLogger('2020sHumorBot').getChild('ImageTweeter')
		
		self.homeDir = homeDir
		self.twitterInteractionCheckInterval = twitterInteractionCheckInterval
	
	def tweetImage(self, imagePath):
		self.logger.debug("tweeting image...")
		bot = self.botClass(self.homeDir, logger = self.logger.getChild("easytweeter"))
		try:
			bot.tweetImage(imagePath)
			bot.checkForUpdates(self.twitterInteractionCheckInterval, directMessages = False)
			
		except Exception as e:
			bot.logger.exception('Exception caused twitter bot to fail.')
			raise e
				
		bot.logger.info("Bot completed successfully.\n")