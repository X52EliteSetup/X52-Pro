help:
	@echo "Elite:Dangerous and Saitek x52/x52Pro helper tool"
	@echo "              -     -    - "
	@echo "It helps you manage the configurations of both things:"
	@echo "deploy     - put the files from the repo to the app folders"
	@echo "collect    - get the files from the app folders to the repo"

deploy:
	python edx52man.py deploy

collect:
	python edx52man.py collect
