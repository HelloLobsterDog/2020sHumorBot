@echo off
rem This is a simple script to delete directories and files generated by python running, setup.py doing it's work, or pyinstaller building.
rem It essentially resets the working directory to a clean slate by deleting all the temporary work files which git is ignoring.

rmdir .\build /S /Q
rmdir .\dist /S /Q
rmdir .\PexelsDownloader\__pycache__ /S /Q
rmdir .\PexelsDownloader.egg-info /S /Q
rmdir .\tests\__pycache__ /S /Q
rmdir .\htmlcov /S /Q
rmdir .\venv /S /Q

del .\MANIFEST
del .\PexelsDownloader.spec
del .\.coverage