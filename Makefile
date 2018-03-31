build:
	docker build -t aptscraper .
run:
	docker container run -v ${APTSCRAPER_CONF}:/work aptscraper aptscraper kj
	docker container run -v ${APTSCRAPER_CONF}:/work aptscraper aptscraper cl

