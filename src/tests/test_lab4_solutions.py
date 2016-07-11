#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# DON'T CHEAT!!!!!!
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
import os

import numpy as np
import pytest
import pandas as pd

from src.features.preprocess_solution import clean_raw_data
from src.features.preprocess_solution import replace_value_with_grouped_mean


@pytest.fixture()
def df():
    """
    read in the raw data file and return the dataframe.
    """
    path, _ = os.path.split(os.path.abspath(__file__))
    project_path = os.path.join(path, os.pardir, os.pardir)

    values_path = os.path.join(project_path, "data", "raw", "pumps_train_values.csv")
    labels_path = os.path.join(project_path, "data", "raw", "pumps_train_labels.csv")

    train = pd.read_csv(values_path, index_col='id', parse_dates=["date_recorded"])
    labels = pd.read_csv(labels_path, index_col='id')

    return train.join(labels)


def test_df_fixture(df):
    assert df.shape == (59400, 40)

    useful_columns = ['amount_tsh',
                      'gps_height',
                      'longitude',
                      'latitude',
                      'region',
                      'population',
                      'construction_year',
                      'extraction_type_class',
                      'management_group',
                      'quality_group',
                      'source_type',
                      'waterpoint_type',
                      'status_group']

    for column in useful_columns:
        assert column in df.columns


def test_clean_raw_data(df):
    """ preprocessing: test the `clean_raw_data` function """
    cleaned_df = clean_raw_data(df)

    # verify construction year
    assert (cleaned_df.construction_year > 1000).all()

    # verify filled in other values
    for numeric_col in ["population", "longitude", "latitude"]:
        assert (cleaned_df[numeric_col] != 0).all()

    # verify the types are in the expected types
    assert (cleaned_df.dtypes
                      .astype(str)
                      .isin(["int64", "float64", "category"])).all()


def test_replace_value_with_grouped_mean(df):
    # in our implementation, replacements happen inplace
    replace_value_with_grouped_mean(df, 0, 'longitude', 'region')
    replace_value_with_grouped_mean(df, 0, 'population', 'region')

    # check an actual values
    np.testing.assert_almost_equal(df.longitude.mean(), 35.14119354200863)
    np.testing.assert_almost_equal(df.population.mean(), 277.3070009774711)


def test_clean_raw_data_cannot_return_missing(df):
    # make an amount_tsh nan
    df.loc[61543, 'amount_tsh'] = np.nan

    with pytest.raises(AssertionError):
        clean_raw_data(df)
