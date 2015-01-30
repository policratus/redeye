help:
	@echo ''
	@echo ''
	@echo '  /__\ ___  __| | ___ _   _  ___ '
	@echo ' / \/// _ \/ _` |/ _ \ | | |/ _ \\'
	@echo '/ _  \  __/ (_| |  __/ |_| |  __/'
	@echo '\/ \_/\___|\__,_|\___|\__, |\___|'
	@echo '                      |___/   '
	@echo ''
	@echo 'Redeye - Computer Vision toolkit'
	@echo ''
	@echo 'Usage: make [options]'
	@echo ''
	@echo 'Options:'
	@echo 'clean - Remove any artifacts'
	@echo 'requirements - Install all dependencies'
	@echo 'build - Build Redeye project'
	@echo 'usage - Show help'

clean:
	find . -iname '*.pyc' -exec rm -f {} +
	find . -type d -iname 'build' -exec rm -rf {} +

requirements:
	pip install -q -r setup/requirements.txt

install:
	python setup/setup.py

build:
	python setup/setup.py build

usage:
	python main/main.py -h
