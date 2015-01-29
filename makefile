help:
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
	@echo 'redeye - Run Redeye'

clean:
	find . -iname '*.pyc' -exec rm -f {} +
	find . -type d -iname 'build' -exec rm -rf {} +

requirements:
	pip install -q -r requirements.txt

install:
	python setup.py
