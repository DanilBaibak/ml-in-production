SHELL=/bin/bash

pull:
	@docker pull dbaibak/docker_airflow:latest

init_config:
	cp config.env.public config.env
	cp docker/scripts/config.ini.public docker/scripts/config.ini

build:
	docker build ./docker -t dbaibak/docker_airflow

up:
	docker-compose up
	docker ps

up_d:
	docker-compose up -d
	docker ps

stop:
	docker-compose stop

down:
	docker-compose down --rmi local --volumes
	make clean

bash:
	docker exec -it airflow_pipeline bash -c "cd airflow_home; bash"

clean_airflow:
	rm -rf */airflow-webserver*
	rm -rf */airflow.cfg
	rm -rf */unittests.cfg

clean:
	make clean_airflow
	find . | grep -E "(__pycache__|\.pyc|\.pyo$\)" | xargs rm -rf
	rm -rf .mypy_cache
	rm -rf .pytest_cache
