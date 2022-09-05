migrations:
	alembic revision --autogenerate -m "$(message)"

migrate:
	alembic upgrade head

docker-build:
	docker build -t milkrage .

docker-run:
	docker run --rm \
		--name milkrage \
		-p 127.0.0.1:5001:5001 \
		milkrage
