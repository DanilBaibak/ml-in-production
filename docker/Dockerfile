FROM python:3.7-slim

RUN apt-get update && apt-get upgrade -y
# install apt packages
RUN mkdir -p /usr/share/man/man1 && mkdir -p /usr/share/man/man7 \
    && apt-get install -y apt-utils postgresql-client libpq-dev make sudo vim gcc \
    && apt autoremove -y \
    && rm -rf /var/lib/apt/lists/*

ENV WORK_DIR="/home"
ENV AIRFLOW_HOME="${WORK_DIR}/airflow_home"
ENV DOCKER_SCRIPTS="${WORK_DIR}/scripts"
ENV PYTHONPATH="${PYTHONPATH}:${AIRFLOW_HOME}:${WORK_DIR}"

WORKDIR $WORK_DIR

COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel && pip install --progress-bar off -r requirements.txt

COPY scripts ${DOCKER_SCRIPTS}/

COPY .bash_history .bash_history/
COPY configs/.bashrc /root/.bashrc

CMD ./scripts/entrypoint.sh
