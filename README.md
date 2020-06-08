# Machine Learning in production using Apache Airflow

To build a solution using Machine Learning is a complex task by itself. Whilst academic Machine Learning has its roots in research from the 1980s, the practical implementation of Machine Learning Systems in production is still relatively new.

This project is an example of how you can improve the two parts of any Machine Learning project - Data Validation and Model Evaluation. The goal is to share practical ideas, that you can introduce in your project relatively simple, but still achieve great benefits.

* **Data Validation** is the process of ensuring that data is present, correct, and meaningful. Ensuring the quality of your data through automated validation checks is a critical step in building data pipelines at any organization.
* **Model validation** occurs after you successfully train the model given the new data. We evaluate and validate the model before it's promoted to production. Ideally, the offline model validation step should include.

<p align="center">
  <img src="https://github.com/DanilBaibak/ml-in-production/blob/master/images/ml_pipeline.png" width="300" title="Machine Learnig Pipeline">
</p>

You can read more details in the [article on Medium]().

## Installation

The project is dockerized and you have two options to run it:
* `make pull` - the [prebuilt image](https://hub.docker.com/r/dbaibak/docker_airflow) will be pulled from the Docker Hub;
* `make build` - you can also build the [Docker image](https://github.com/DanilBaibak/ml-in-production/tree/master/docker) by yourself;
* `make init_config` will initialize all necessary configs;
* `make up_d` will start up your application detached mode. After the application is started, you can easily have access to the project by the link http://localhost:8080/

## Useage

* `make bash` will create a new Bash session in the container.
* `make stop` stops running containers without removing them.
* `make down` stops and removes containers.
