build-base:
	docker build -t donna-py -f Dockerfile.python .

test:
	docker-compose run test flake8
	docker-compose run test pytest

