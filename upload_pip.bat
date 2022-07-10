@echo off
rem this is a simple script that builds and uploads to pip

echo cleaning...
call clean.bat

echo building distributions...
python setup.py sdist bdist_wheel

echo Pausing. Inspect the above output. Ctrl-C to terminate if you have concerns about the quality of the code about to be uploaded.
pause

echo Uploading...
twine upload dist/*

echo Upload complete!
pause