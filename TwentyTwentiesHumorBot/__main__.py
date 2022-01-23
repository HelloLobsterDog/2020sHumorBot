#!/usr/bin/env python

import sys
import os

def main():
	if (__package__ is None or __package__ == "") and not hasattr(sys, 'frozen'):
		# direct call of __main__.py
		import os.path
		path = os.path.realpath(os.path.abspath(__file__))
		sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

	import TwentyTwentiesHumorBot
	TwentyTwentiesHumorBot.main()

if __name__ == '__main__':
	main()
