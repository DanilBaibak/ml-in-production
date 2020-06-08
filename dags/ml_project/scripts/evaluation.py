import logging
from pathlib import Path, PosixPath
import pandas as pd
from datetime import date
from joblib import load

from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error

from dags.ml_project.scripts.trainig import MODEL_PATH
from dags.ml_project.scripts.trainig import _get_data


def evaluate():
    """
    Evaluate the model using the training data. It also logs the metadata of the ML pipeline.
    :return:
    """
    df, target = _get_data()
    model_path = Path(MODEL_PATH)
    model = _load_model(model_path.joinpath(f'model_{date.today().isoformat()}.joblib'))

    _evaluate_model(model, df, target)
    _logging_model_params(model, df)


def _load_model(model_path: PosixPath) -> Pipeline:
    """
    Load the pre-trained model.

    :param model_path:
    :return Pipeline: uncompressed Pipeline
    """
    return load(model_path)


def _evaluate_model(model: Pipeline, df: pd.DataFrame, target: list):
    """
    For the evaluation, we use mean_squared_error and mean_absolute_error loss functions.

    :param model:
    :param df:
    :param target:
    :return:
    """
    predictions = model.predict(df)

    logging.info(f'### Mean squared error: {mean_squared_error(target, predictions)}')
    logging.info(f'### Mean absolute error: {mean_absolute_error(target, predictions)}')


def _logging_model_params(model: Pipeline, df: pd.DataFrame):
    """
    Logs the metadata of the pipeline.

    :param model:
    :param df:
    :return:
    """
    transformers = model.named_steps['preprocessor'].transformers_

    # numerical features
    numerical_feature_attrs = transformers[0][1].named_steps['scaler']
    logging.info(f'### Scale of the numerical features: {numerical_feature_attrs.scale_}')
    logging.info(f'### Mean of the numerical features: {numerical_feature_attrs.mean_}')

    # categorical features
    features_categorical = list(df.select_dtypes(include=['category']).columns)
    categorical_feature_attrs = transformers[1][1].named_steps['ohe']
    logging.info(f'### Categorical feature names: {categorical_feature_attrs.get_feature_names(features_categorical)}')

    # feature importances
    logging.info(f'### Feature importances: {model.named_steps["regressor"].feature_importances_}')
