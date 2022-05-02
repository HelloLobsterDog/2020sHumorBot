import unittest
import logging

mainLogger = logging.getLogger('PexelsDownloader')
mainLogger.setLevel(logging.ERROR) # change to debug and the tests will log everything to the console
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
mainLogger.addHandler(sh)
		

loader = unittest.TestLoader()
testSuite = loader.discover('tests')
testRunner = unittest.TextTestRunner(verbosity=2)
testRunner.run(testSuite)
