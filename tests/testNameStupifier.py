import unittest
import random
from TwentyTwentiesHumorBot import NameStupifier

class NameStupifierTests(unittest.TestCase):
	
	def setUp(self):
		random.seed(694201337)
		self.stupifier = NameStupifier()
	
	def testHappyPath(self):
		self.assertEqual(self.stupifier.stupify("goose"), "gossoe") # 2 iterations, flip then replace.
		
	
	def testSimpleReplace(self):
		self.assertEqual(self.stupifier._simpleReplace("goose"), "gooshe")
	
	def testSimpleReplaceNoReplacements(self):
		self.assertEqual(self.stupifier._simpleReplace("qx"), "qx")
	
	def testSimpleReplaceImportantWords(self):
		for word in ['dog', 'cat', 'bear', 'bird', 'person', 'carrot']:
			self.assertNotEqual(self.stupifier._simpleReplace(word), word)
		
	
	
	def testFlipLetters(self):
		self.assertEqual(self.stupifier._flipLetters("goose"), "gooes")
	
	def testFlipLettersShortWords(self):
		self.assertEqual(self.stupifier._flipLetters("asd"), "ads")
		self.assertEqual(self.stupifier._flipLetters("as"), "sa")
		self.assertEqual(self.stupifier._flipLetters("a"), "a")
		
		
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