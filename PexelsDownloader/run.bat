@echo off
rem This is a convenience script to string together runs of the downloader with the keywords I'm looking for.
rem The keywords here were chosen because they tend to result in images that the object recognition library will actually recognize, saving me from needing to override what it comes up with.

python PexelsDownloader --verbose --key-file ..\..\pexels_api_key.ini --dir J:\pexels -n 20 cat