import numpy as np
import pandas as pd


def awesome_function(s):
    from IPython.display import display, HTML
    css = """
        .blink {
            animation-duration: 1s;
            animation-name: blink;
            animation-iteration-count: infinite;
            animation-timing-function: steps(2, start);
        }
        @keyframes blink {
            80% {
                visibility: hidden;
            }
        }"""

    to_show = HTML(
        '<style>{}</style>'.format(css) +
        '<p class="blink"> {} IS AWESOME!!!!! </p>'.format(s)
    )
    display(to_show)


def remove_invalid_data(path):
    """ Takes a path to a water pumps csv, loads in pandas, removes
        invalid columns and returns the dataframe.
    """
    df = pd.read_csv(path, index_col=0)

    # preselected columns
    useful_columns = ['amount_tsh',
                      'gps_height',
                      'longitude',
                      'latitude',
                      'region',
                      'population',
                      'construction_year',
                      'extraction_type_class',
                      'status_group',
                      'management_group',
                      'quality_group',
                      'source_type',
                      'waterpoint_type']

    df = df[useful_columns]

    invalid_values = {
        'amount_tsh': {0: np.nan},
        'longitude': {0: np.nan},
        'installer': {0: np.nan},
        'construction_year': {0: np.nan},
    }

    # drop rows with invalid values
    df.replace(invalid_values, inplace=True)

    # drop any rows in the dataset that have NaNs
    df.dropna(how="any")

    # create categorical columns
    for c in df.columns:
        if df[c].dtype == 'object':
            df[c] = df[c].astype('category')

    df.drop('status_group')

    return pd.get_dummies(df)

def gimme_the_mean(series):
    if isinstance(series, float):
        return series

    return np.mean(series)
