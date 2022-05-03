import os
import os.path
import logging

import requests
from pexels_api import API

class PexelsDownloader(object):
	def __init__(self, apiKey, folder, downloadedPath = ""):
		self.logger = logging.getLogger('PexelsDownloader')
		self.api = API(apiKey)
		self.folder = folder
		self.downloadedPath = downloadedPath
		
		# make the folder if it doesn't exist
		os.makedirs(self.folder, exist_ok = True)
		
		# load downloaded files
		self.downloaded = []
		if self.downloadedPath and os.path.exists(self.downloadedPath):
			self.logger.debug("loading downloaded ids list from file: %s", self.downloadedPath)
			with open(self.downloadedPath, 'r') as f:
				for id in f:
					if len(id.strip()) > 0:
						self.downloaded.append(str(id).strip())
			self.logger.debug("Successfully loaded %s ids from file.", len(self.downloaded))
		else:
			self.logger.debug("downloaded id list file not found.")
		
	def download(self, searchKey, totalImages = 50, imagesPerPage = 10):
		self.api.search(searchKey, imagesPerPage)
		
		if not self.api.json['photos']:
			raise RuntimeError("api returned no photos from the request.")
		else:
			downloaded = 0
			while downloaded < totalImages:
				for photo in self.api.get_entries():
					self.logger.debug('attempting to download image %s from entry: %s', downloaded, photo)
					self.downloadPhoto(photo, searchKey)
					downloaded += 1
				self.logger.debug("reached end of page.")
				if not self.api.search_next_page():
					self.logger.warning("Reached end of search results before reaching desired number of images.")
					break
			self.logger.info("successfully crawled " + str(downloaded) + " photos.")
		
		self.saveDownloadList()
	
	def saveDownloadList(self):
		if self.downloadedPath:
			self.logger.debug("saving downloaded ids list to file: %s", self.downloadedPath)
			with open(self.downloadedPath, 'w') as f:
				for id in self.downloaded:
					f.write(str(id))
					f.write("\n")
			self.logger.debug("Successfully saved %s ids to file.", len(self.downloaded))
		else:
			self.logger.debug("skipping saving download list, because file is not set.")
		
	def downloadPhoto(self, photo, searchUsed):
		path = os.path.join(self.folder, self.determinePhotoFilename(photo, searchUsed))
		url = photo.original
		
		if not self.photoAlreadyDownloaded(photo):
			self.logger.info("Downloading photo from url " + url + " to file: " + path)
			with open(path, "wb") as f:
				try:
					f.write(requests.get(url, timeout=15).content)
					self.downloaded.append(str(photo.id))
					self.logger.info("successfully downloaded url: " + url)
				except:
					self.logger.exception("Exception encountered while attempting to download url: " + url)
		else:
			self.logger.info("url " + url + " has already been downloaded.")
	
	def determinePhotoFilename(self, photo, searchUsed):
		path = "pexels - " + str(photo.id) + " - " + photo.photographer.replace(" ", "_") + " - '" + searchUsed + "'"
		path += "." + photo.extension if not photo.extension == "jpeg" else ".jpg"
		return path
	
	def photoAlreadyDownloaded(self, photo):
		return str(photo.id) in self.downloaded