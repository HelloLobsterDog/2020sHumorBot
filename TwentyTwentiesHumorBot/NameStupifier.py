import logging

class NameStupifier(object):
	def __init__(self):
		self.logger = logging.getLogger('2020sHumorBot').getChild('NameStupifier')
		
	def stupify(self, name):
		return name # TODO