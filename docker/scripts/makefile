#!/usr/bin/env bash
SHELL=/bin/bash

init_airflow:
	make clean_airflow
	airflow initdb
	airflow version

run_airflow:
	airflow webserver -D
	cd ${AIRFLOW_HOME} && airflow scheduler

clean_airflow:
	rm -rf ${AIRFLOW_HOME}/airflow.cfg
	rm -rf ${AIRFLOW_HOME}/airflow-webserver*
	rm -rf ${AIRFLOW_HOME}/unittests.cfg
