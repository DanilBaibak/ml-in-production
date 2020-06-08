from pathlib import Path, PosixPath
import numpy as np
import pandas as pd
import logging
from datetime import date
from joblib import dump

from sklearn.datasets import load_boston
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor

SEED = 42
MODEL_PATH = 'dags/ml_project/models/'

np.random.seed(SEED)


def training():
    """
    Get data, build pipeline, train the model.
    """
    df, target = _get_data()
    model = _build_ml_pipeline(df)

    model.fit(df, target)
    _save_model(model, Path(MODEL_PATH))


def _get_data():
    """
    Use the toy dataset from sklearn.
    (https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_boston.html)
    :return:
    """
    data = load_boston()

    df = pd.DataFrame(data=data['data'], columns=data['feature_names'])
    # set the category type for the categorical properties
    df.CHAS = df.CHAS.astype(np.int16).astype('category')
    df.RAD = df.RAD.astype(np.int16).astype('category')

    # get target values
    target = data['target']

    logging.info(f'### Data shape: {df.shape}')

    return df, target


def _build_ml_pipeline(df: pd.DataFrame) -> Pipeline:
    """
    Builds ML pipeline using sklearn.

    :param df: the data frame of the features.
    :return Pipeline:
    """
    features_numerical = list(df.select_dtypes(include=['float64']).columns)
    features_categorical = list(df.select_dtypes(include=['category']).columns)

    logging.info(f'### A number of numerical features: {len(features_numerical)}')
    logging.info(f'### A number of categorical features: {len(features_categorical)}')

    # transformers
    transformer_numerical = Pipeline(steps=[('scaler', StandardScaler())])
    transformer_categorical = Pipeline(steps=[('ohe', OneHotEncoder(handle_unknown='ignore'))])

    # processor
    preprocessor = ColumnTransformer(transformers=[('numerical', transformer_numerical, features_numerical),
                                                   ('categorical', transformer_categorical, features_categorical)])

    # full pipeline
    model = Pipeline(steps=[('preprocessor', preprocessor),
                            ('regressor', RandomForestRegressor(n_estimators=250, random_state=SEED))])

    return model


def _save_model(model: Pipeline, model_path: PosixPath):
    """
    Saves the trained model with the sufix of the current day in the name of the file.

    :param model:
    :param model_path:
    :return:
    """
    path = model_path.joinpath(f'model_{date.today().isoformat()}.joblib')
    dump(model, path)
