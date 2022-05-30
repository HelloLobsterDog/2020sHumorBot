import logging
import re

class NameStupifier(object):
	def __init__(self, rand):
		self.logger = logging.getLogger('2020sHumorBot').getChild('NameStupifier')
		self.rand = rand
		
		self.minIterations = 1
		self.maxIterations = 2
		self.stupifiers = [self._simpleReplace, self._flipLetters]
		
		# simple replace
		self.simpleReplaceMap = [(re.compile(x[0]), x[1]) for x in [
				('oo', 'ü'),
				('b', 'p'), ('p', 'b'),
				('f', 'v'), ('v', 'f'), 
				('f', 'th'),
				('f', 'ph'), ('ph', 'f'),
				('s', 'z'), ('z', 's'),
				('s', 'ss'),
				('t', 'b'), ('b', 't'),
				('m', 'n'), ('n', 'm'),
				('qu', 'kw'),
				('ea', 'ee'),
				('a', 'uh'),
				('r', 'rr'),
				('y', 'ee'),
				('ck', 'cc'),
				('j', 'ch'), ('ch', 'j'),
				('j', 'g'),
				('s', 'sh'), ('sh', 's'),
				('n', 'ñ'),
				('ee', 'e'),
				('oo', 'o'), ('o', 'oo')
		]]
		
	def stupify(self, name):
		iterations = self.rand.randrange(self.minIterations, self.maxIterations + 1)
		self.logger.info("Stupifying name '" + name + "' with " + str(iterations) + " iterations.")
		for i in range(iterations):
			name = self.rand.choice(self.stupifiers)(name)
			self.logger.info("Stupified name after iteration " + str(i + 1) + ": " + name)
		return name
	
	
	def _simpleReplace(self, name):
		# narrow down to entries we can do
		viable = []
		for possible in self.simpleReplaceMap:
			if possible[0].search(name) != None:
				viable.append(possible)
		# actually do the replace
		if viable:
			self.logger.debug("name '" + name + "' has " + str(len(viable)) + " possible replacements: " + str(viable))
			replacement = self.rand.choice(viable)
			self.logger.info("Making replacement in name '" + name + "': '" + str(replacement[0].pattern) + "'->'" + replacement[1] + "'")
			return replacement[0].sub(replacement[1], name)
		else:
			self.logger.warning("unable to find a simple replace match for name: " + name)
			return name
			
	def _flipLetters(self, name):
		if len(name) < 2: # can't flip two letters if there aren't two letters
			return name
		start = self.rand.randrange(len(name)-1)
		self.logger.info("flipping letters in name " + name + " at index " + str(start))
		before = name[:start]
		after = name[start+2:]
		self.logger.debug(before + " + " + name[start+1:start+2] + " + " + name[start:start+1] + " + " + after)
		return before + name[start+1:start+2] + name[start:start+1] + after