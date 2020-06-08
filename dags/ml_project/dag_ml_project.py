from datetime import datetime

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.check_operator import CheckOperator, IntervalCheckOperator, ValueCheckOperator

from dags.ml_project.scripts.trainig import training
from dags.ml_project.scripts.evaluation import evaluate

CONN_ID = 'dev_postgres'


with DAG(
    dag_id='ml_project',
    description='ML project',
    schedule_interval='0 8 * * *',
    start_date=datetime(2020, 1, 6)
) as dag:
    enter_point = DummyOperator(
        task_id='enter_point'
    )

    check_interaction_data = CheckOperator(
        task_id='check_interaction_data',
        sql='SELECT COUNT(1) FROM interaction WHERE interaction_date = CURRENT_DATE',
        conn_id=CONN_ID
    )

    check_interaction_intervals = IntervalCheckOperator(
        task_id='check_interaction_intervals',
        table='interaction',
        metrics_thresholds={'COUNT(*)': 1.5,
                            'MAX(amount)': 1.3,
                            'MIN(amount)': 1.4,
                            'SUM(amount)': 1.3},
        date_filter_column='interaction_date',
        days_back=5,
        conn_id=CONN_ID
    )

    check_interaction_amount_value = ValueCheckOperator(
        task_id='check_interaction_amount_value',
        sql="SELECT COUNT(1) FROM interaction WHERE interaction_date=CURRENT_DATE - 1",
        pass_value=200,
        tolerance=0.2,
        conn_id=CONN_ID
    )

    check_unique_products_value = ValueCheckOperator(
        task_id='check_unique_products_value',
        sql="SELECT COUNT(DISTINCT(product_id)) FROM interaction WHERE interaction_date=CURRENT_DATE - 1",
        pass_value=150,
        tolerance=0.3,
        conn_id=CONN_ID
    )

    check_replaced_amount_value = ValueCheckOperator(
        task_id='check_replaced_amount_value',
        sql="""
            SELECT count(1)
            FROM interaction
            WHERE interaction_date > CURRENT_DATE - 7
                AND interaction_type = 'replaced'""",
        pass_value=60,
        tolerance=0.3,
        conn_id=CONN_ID
    )

    train_model = PythonOperator(
        task_id='train_model',
        python_callable=training
    )

    evaluate_model = PythonOperator(
        task_id='evaluate_model',
        python_callable=evaluate
    )

    checks = [check_interaction_data,
              check_interaction_intervals,
              check_interaction_amount_value,
              check_unique_products_value,
              check_replaced_amount_value]

    enter_point >> checks >> train_model >> evaluate_model
