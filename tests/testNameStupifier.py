import unittest
import random
from TwentyTwentiesHumorBot import NameStupifier

class NameStupifierTests(unittest.TestCase):
	
	def setUp(self):
		random.seed(694201337)
		self.stupifier = NameStupifier()
	
	def testHappyPath(self):
		self.assertEqual(self.stupifier.stupify("goose"), "goshoe")
	
	def testSimpleReplace(self):
		self.assertEqual(self.stupifier._simpleReplace("goose"), "gooshe")
	
	def testFlipLetters(self):
		self.assertEqual(self.stupifier._flipLetters("goose"), "gooes")
		
	def manyWords(self): # add test to the name of this to do some manual QA on the output
		random.seed()
		words = []
		with open('..\\englishDictionary.txt') as file:
			for word in file:
				words.append(word.strip())
		stupid = []
		for x in range(20):
			word = random.choice(words)
			stupid.append(word + " -> " + self.stupifier.stupify(word))
		for x in stupid:
			print(x)