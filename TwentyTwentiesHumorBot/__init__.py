import argparse
import os
import os.path
import sys
import logging
import logging.handlers

from .TwentyTwentiesHumorBot import TwentyTwentiesHumorBot

__version__ = '0.0.2'



def parseArgs():
	parser = argparse.ArgumentParser(description="A Twitter bot which posts humor which only those in 2020 find humorous.")
	
	verbosityGroup = parser.add_mutually_exclusive_group()
	verbosityGroup.add_argument('-v', '--verbose', action="store_true", help = "All logs will be printed to stdout.")
	verbosityGroup.add_argument('-q', '--quiet', action="store_true", help = "All output to stdout and stderr will be disabled.")
	
	parser.add_argument('--home-directory', '-d', default='~/.2020sHumorBot',
						help = "Specifies the bot's home directory, in which it will place the logs and read the model, configs and input images from.")
						
	parser.add_argument('--log-level', choices = ['NOT_SET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='INFO',
						help = 'Specifies the log level of the bot log file. Defaults to INFO.')
	
	return parser.parse_args()
	
def parseLogLevel(arg):
	if arg == 'NOT_SET':
		return logging.NOTSET
	elif arg == 'DEBUG':
		return logging.DEBUG
	elif arg == 'INFO':
		return logging.INFO
	elif arg == 'WARNING':
		return logging.WARNING
	elif arg == 'ERROR':
		return logging.ERROR
	elif arg == 'CRITICAL':
		return logging.CRITICAL
		
	elif arg == None:
		return logging.INFO
	else:
		raise RuntimeError('log level argument "{}" not recognized'.format(arg))
	
def makeLoggers(homeDir, logLevel, verbose):
	# make log directory first, if it does not exist
	logDir = os.path.normpath(os.path.join(homeDir, 'logs'))
	os.makedirs(logDir, exist_ok = True)
	# actual log file
	realLogFile = os.path.normpath(os.path.join(logDir, '2020sHumorBot.log'))
	
	# main log
	mainLogger = logging.getLogger('2020sHumorBot')
	mainLogger.setLevel(parseLogLevel(logLevel))
	# file
	fh = logging.handlers.TimedRotatingFileHandler(realLogFile, when = 'midnight', encoding = 'utf-8')
	fh.setLevel(logging.DEBUG)
	fh.setFormatter(logging.Formatter('%(asctime)s [%(levelname)-5s] %(name)s: %(message)s'))
	mainLogger.addHandler(fh)
	# console
	if verbose:
		sh = logging.StreamHandler()
		sh.setLevel(logging.DEBUG)
		sh.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
		mainLogger.addHandler(sh)


def main():
	args = parseArgs()
	
	if args.verbose:
		verbose = True # --verbose specified
	elif args.quiet:
		verbose = False # --quiet specified
	else:
		verbose = True # neither --verbose or --quiet specified, so do the default
	
	
	makeLoggers(args.home_directory, args.log_level, verbose)
	
	bot = TwentyTwentiesHumorBot(args.home_directory)
	
	success = bot.run()
	
	if success:
		sys.exit(0)
	else:
		sys.exit(1)