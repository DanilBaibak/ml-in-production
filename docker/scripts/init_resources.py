from os import system, environ
import configparser
import psycopg2
from psycopg2.extras import execute_values

from datetime import date, timedelta
import numpy as np

SEED = 42
# VARIABLES_PREFIX = 'VAR__'

NUMBER_OF_DAYS = 7
NUMBER_OF_USERS = 1000
NUMBER_OF_ITEMS = 300
NUMBER_OF_SALES = 200

np.random.seed(SEED)


# def init_airflow_resources():
#     """
#     Set the airflow variables.
#     """
#     keys_with_prefix = _filter_keys(VARIABLES_PREFIX)
#     for key in keys_with_prefix:
#         command = f'airflow variables --set {key[len(VARIABLES_PREFIX):]} "{environ[key]}"'
#         exec_cli(command)


def set_up_db():
    """
    Setup the database and fills it in with the fixtures.
    All data is synthetic and used solely for indicative purposes.
    """
    config = _get_config('config.ini')
    conn = psycopg2.connect(dbname=config.get('postgres_db', 'dbname'),
                            user=config.get('postgres_db', 'user'),
                            password=config.get('postgres_db', 'password'),
                            host=config.get('postgres_db', 'host'))
    _create_table(conn)
    _fill_in_interactions(conn)

    conn.close()


def exec_cli(command: str):
    """
    Execute a command in a subshell.

    :param command: a shell command
    """
    result = system(command)
    if result:
        raise Exception(f'Command execution error: {result}')


def _get_config(path: str) -> configparser.ConfigParser:
    """
    Get the config of the project.

    :param path: a path to the config
    :return:
    """
    config = configparser.ConfigParser()
    config.read(path)

    return config


def _filter_keys(prefix):
    return list(filter(lambda key: key.startswith(prefix), environ.keys()))


def _create_table(conn):
    """
    Create the necessary tables.

    :param conn:
    :return:
    """
    cursor = conn.cursor()

    with open('sql/tables.sql', 'r') as f:
        cursor.execute(f.read())

    conn.commit()
    cursor.close()


def _fill_in_interactions(conn):
    """
    Fill in tables.

    :param conn:
    :return:
    """
    cursor = conn.cursor()
    # remove data if exists
    cursor.execute('TRUNCATE TABLE interaction;')
    # insert fresh data
    query = 'INSERT INTO interaction (customer_id, product_id, amount, interaction_type, interaction_date) VALUES %s'
    data = _get_interactions_data()

    execute_values(cursor, query, data)

    conn.commit()
    cursor.close()


def _get_interactions_data() -> list:
    """
    Generate data for the examples.

    :return:
    """
    i = NUMBER_OF_DAYS
    data = []

    while i >= 0:
        interaction_date = (date.today() - timedelta(days=i)).isoformat()
        number_of_sales = np.random.randint(low=NUMBER_OF_SALES-30, high=NUMBER_OF_SALES+30, size=1)[0]

        interaction_dates = np.array([interaction_date for _ in range(number_of_sales)])
        users_data = np.random.randint(low=0, high=NUMBER_OF_USERS, size=(number_of_sales,))
        items_data = np.random.randint(low=0, high=NUMBER_OF_ITEMS, size=(number_of_sales,))
        amount_data = np.random.randint(low=900, high=1300, size=(number_of_sales,))
        interaction_types = np.random.choice(['bought', 'returned', 'replaced'],
                                             size=number_of_sales,
                                             p=[0.9, 0.05, 0.05])

        for j in range(number_of_sales):
            data.append(tuple([int(users_data[j]),
                               int(items_data[j]),
                               int(amount_data[j]),
                               interaction_types[j],
                               interaction_dates[j]]))
        i -= 1

    return data


if __name__ == '__main__':
    # init_airflow_resources()
    set_up_db()
