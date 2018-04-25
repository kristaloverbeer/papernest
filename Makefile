build:
	@docker-compose --project-directory ./ -f docker/docker-compose.yml build --no-cache
run: build
	@docker-compose --project-directory ./ -f docker/docker-compose.yml up -d
sh:
	@docker exec -it api /bin/sh
upgrade:
	@docker exec -it api flask db upgrade
typing-check:
	@docker exec -it api mypy src/ --ignore-missing-imports
syntax-check:
	@docker exec -it api flake8
tests:
	@docker exec -it api pytest
stop:
	@docker-compose --project-directory ./ -f docker/docker-compose.yml stop
clean: stop
	@docker-compose --project-directory ./ -f docker/docker-compose.yml rm -vf api
clean-dangling-images: clean
	@docker rmi -f $(docker images -q --filter "dangling=true")

.PHONY: build run sh upgrade typing-check syntax-check tests stop clean clean-dangling-images
