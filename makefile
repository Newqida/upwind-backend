build-dev:
	docker-compose build

run-dev:
	docker-compose up

superuser-dev:
	docker-compose run --rm web python manage.py createsuperuser

build-prod:
	docker-compose -f docker-compose.prod.yml build

run-prod:
	docker-compose -f docker-compose.prod.yml up

superuser-prod:
	docker-compose -f docker-compose.prod.yml run --rm sut python manage.py createsuperuser

test:
	docker-compose run --rm web /test.sh

test-ci:
	docker-compose -f docker-compose.prod.yml run --rm sut /test.sh