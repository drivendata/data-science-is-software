import os

import pandas as pd

from .build_features import remove_invalid_data

PROJ_ROOT = os.path.join(__file__,
                         os.pardir,
                         os.pardir,
                         os.pardir)

PROJ_ROOT = os.path.abspath(PROJ_ROOT)


def test_remove_invalid_data():
    data_path = os.path.join(PROJ_ROOT,
                             "data",
                             "raw",
                             "training_values.csv")

    df = remove_invalid_data(data_path)

    assert pd.notnull(df.values).all(axis=(0, 1))
