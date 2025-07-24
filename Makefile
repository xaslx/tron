.PHONY: app app-down app-logs alembic-revision alembic-upgrade


app:
	docker-compose up -d --build

app-down:
	docker-compose down

app-logs:
	docker-compose logs -f app


alembic-revision:
	docker exec -it tron-app alembic revision --autogenerate


alembic-upgrade:
	docker exec -it tron-app alembic upgrade head