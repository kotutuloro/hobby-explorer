dev:
	docker-compose up

test:
	docker-compose -f docker-compose.test.yml run --rm test

