import numpy as np
import pandas as pd


def remove_invalid_data(path):
    """ Takes a path to a water pumps csv, loads in pandas, removes
        invalid columns and returns the dataframe.
    """
    df = pd.read_csv(path, index_col=0)

    invalid_values = {
        'amount_tsh': {0: np.nan},
        'longitude': {0: np.nan},
        'installer': {0: np.nan},
        'construction_year': {0: np.nan},
    }

    # drop rows with invalid values
    df.replace(invalid_values, inplace=True)
    df.dropna(how="any", inplace=True)

    return df


def gimme_the_mean(series):
    if isinstance(series, float):
        return series

    return np.mean(series)
