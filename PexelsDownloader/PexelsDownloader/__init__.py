import argparse
import os
import os.path
import sys
import logging
import logging.handlers
import configparser
import codecs

from .PexelsDownloader import PexelsDownloader

__version__ = '0.1.0'



def parseArgs():
	parser = argparse.ArgumentParser(description="A program which bulk downloads photos from pexels.com, given a search query")
	
	verbosityGroup = parser.add_mutually_exclusive_group()
	verbosityGroup.add_argument('-v', '--verbose', action="store_true", help = "All messages, including debugging messages, will be logged.")
	verbosityGroup.add_argument('-q', '--quiet', action="store_true", help = "Only important messages will be logged.")
	
	parser.add_argument('--dir', '-d', help = "Specifies the directory into which downloaded photos are written.")
	
	parser.add_argument('--log-dir', default = "", help = 'Logs will be written to the directory provided. By default, logs are only written to stdout.')
	
	parser.add_argument("--number", '-n', default=50, type=int, help = "Number of photos to download.")
	parser.add_argument("--number-per-page", default=10, type=int, help = "Number of photos to download per page. Setting this correctly helps avoid taxing pexel's servers too much, but it does not usually require modification.")
	
	parser.add_argument("--key-file", '-k', help="ini config file containing the pexels api key to use.")
	
	parser.add_argument('query', help = 'The string to search for on pexels.')
	
	return parser.parse_args()
	
def makeLoggers(logDirectory, logDir, verbose):
	mainLogger = logging.getLogger('PexelsDownloader')
	if verbose:
		mainLogger.setLevel(logging.DEBUG)
	else:
		mainLogger.setLevel(logging.INFO)
	
	# console
	sh = logging.StreamHandler()
	sh.setLevel(logging.DEBUG)
	sh.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
	mainLogger.addHandler(sh)
	
	if logDirectory:
		# make log directory first, if it does not exist
		os.makedirs(logDirectory, exist_ok = True)
		# actual log file
		realLogFile = os.path.normpath(os.path.join(logDirectory, 'PexelsDownloader.log'))
		# file
		fh = logging.handlers.TimedRotatingFileHandler(realLogFile, when = 'midnight', encoding = 'utf-8')
		fh.setLevel(logging.DEBUG)
		fh.setFormatter(logging.Formatter('%(asctime)s [%(levelname)-5s] %(name)s: %(message)s'))
		mainLogger.addHandler(fh)
	
def loadKey(path):
	config = configparser.ConfigParser()
	config.read_file(codecs.open(path, 'r', 'utf8'))
	return config['PexelsAPI']['key']


def main(overrideCuration = False):
	args = parseArgs()
	
	if args.verbose:
		verbose = True # --verbose specified
	elif args.quiet:
		verbose = False # --quiet specified
	else:
		verbose = True # neither --verbose or --quiet specified, so do the default
	
	makeLoggers(args.log_dir, args.log_dir, verbose)
	
	try:
		downloader = PexelsDownloader(loadKey(args.key_file), args.dir)
		downloader.download(args.query, totalImages = args.number, imagesPerPage = args.number_per_page)
		success = True
	except Exception as e:
		logging.getLogger('PexelsDownloader').exception("Exception encountered while attempting to download.")
		success = False
	
	if success:
		sys.exit(0)
	else:
		sys.exit(1)
		