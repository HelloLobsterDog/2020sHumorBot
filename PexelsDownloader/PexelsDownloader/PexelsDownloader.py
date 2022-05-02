import os
import os.path
import logging

import requests
from pexels_api import API

class PexelsDownloader(object):
	def __init__(self, apiKey, folder):
		self.logger = logging.getLogger('PexelsDownloader')
		self.api = API(apiKey)
		self.folder = folder
		
		# make the folder if it doesn't exist
		os.makedirs(self.folder, exist_ok = True)
		
	def download(self, searchKey, totalImages = 50, imagesPerPage = 10):
		self.api.search(searchKey, imagesPerPage)
		
		if not self.api.json['photos']:
			raise RuntimeError("api returned no photos from the request.")
		else:
			downloaded = 0
			while downloaded < totalImages:
				for photo in self.api.get_entries():
					self.logger.debug('attempting to download image %s from entry: %s', downloaded, photo)
					self.downloadPhoto(photo)
					downloaded += 1
				self.logger.debug("reached end of page.")
				if not self.api.search_next_page():
					self.logger.warning("Reached end of search results before reaching desired number of images.")
					break
			self.logger.info("successfully crawled " + str(downloaded) + " photos.")
		
	def downloadPhoto(self, photo):
		path = str(photo.id) + " - " + photo.photographer.replace(" ", "_")
		path += "." + photo.extension if not photo.extension == "jpeg" else ".jpg"
		path = os.path.join(self.folder, path)
		url = photo.original
		
		if not self.photoAlreadyDownloaded(photo):
			self.logger.info("Downloading photo from url " + url + " to file: " + path)
			with open(path, "wb") as f:
				try:
					f.write(requests.get(url, timeout=15).content)
				except:
					self.logger.exception("Exception encountered while attempting to download url: " + url)
			self.logger.info("successfully downloaded url: " + url)
		else:
			self.logger.info("url " + url + " has already been downloaded.")
	
	def photoAlreadyDownloaded(self, photo):
		# TODO this is a temporary version of the method, which simply checks whether the file's already been downloaded. The future version of this method will read a file containing all ids.
		path = str(photo.id) + " - " + photo.photographer.replace(" ", "_")
		path += "." + photo.extension if not photo.extension == "jpeg" else ".jpg"
		path = os.path.join(self.folder, path)
		return os.path.exists(path)