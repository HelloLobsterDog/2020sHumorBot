@echo off
coverage run --source=PexelsDownloader run_tests.py
coverage html -i
