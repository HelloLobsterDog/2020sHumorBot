import unittest
import logging

mainLogger = logging.getLogger('2020sHumorBot')
mainLogger.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
#mainLogger.addHandler(sh) # uncomment me to make the tests log to the console
		

loader = unittest.TestLoader()
testSuite = loader.discover('tests')
testRunner = unittest.TextTestRunner(verbosity=2)
testRunner.run(testSuite)
