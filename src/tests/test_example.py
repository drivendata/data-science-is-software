# -*- coding: utf-8 -*-
import pytest
import numpy as np
import pandas as pd

from .example import replace_all_nulls_with_value


@pytest.fixture
def df_none_missing():
    """ return a 3x3 dataframe with no missing values """
    cols = ['a', 'b', 'c']
    data = [[0, 1, 0], [0, 0, 1], [1, 1, 1]]
    return pd.DataFrame(data, columns=cols)


@pytest.fixture
def df_missing():
    """ return a 3x3 dataframe with a couple of NaNs """
    df = df_none_missing()
    df.ix[0, 2] = np.nan
    df.ix[2, 1] = np.nan
    return df


def test_replace_all_nulls_does_nothing_if_no_nulls(df_none_missing):
    new_df = replace_all_nulls_with_value(df_none_missing, -1)
    assert (df_none_missing.values == new_df.values).all()
    assert pd.notnull(new_df.values).all()


def test_replace_all_nulls(df_missing):
    n_null_before = pd.isnull(df_missing.values).sum()
    assert n_null_before == 2

    new_df = replace_all_nulls_with_value(df_missing, -1)
    n_null_after = pd.isnull(new_df.values).sum()
    assert n_null_after == 0

    assert pd.notnull(new_df.values).all()


def test_engarde_rejects_replacing_nulls_with_nulls(df_missing):
    with pytest.raises(AssertionError):
        replace_all_nulls_with_value(df_missing, np.nan)
