#!/usr/bin/env bash

PYTHONPATH=$PYTHONPATH:$DOCKER_SCRIPTS

cd ${DOCKER_SCRIPTS}

make init_airflow

python init_resources.py

make run_airflow
