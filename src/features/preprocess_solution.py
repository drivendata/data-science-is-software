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
from engarde.decorators import none_missing


@none_missing()
def clean_raw_data(df):
    """ Takes a dataframe and performs four steps:
            - Selects columns for modeling
            - For numeric variables, replaces 0 values with mean for that region
            - Fills invalid construction_year values with the mean construction_year
            - Converts strings to categorical variables

        :param df: A raw dataframe that has been read into pandas
        :returns: A dataframe with the preprocessing performed.
    """
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

    zero_is_bad_value = ['longitude', 'population']

    other_bad_value = ['latitude']

    # subset to columns we care about
    df = df[useful_columns]

    for column, column_type in df.dtypes.iteritems():
        # special case construction year
        if column == 'construction_year':
            invalid_rows = df.construction_year < 1000
            valid_mean = int(df.construction_year[~invalid_rows].mean())
            df.loc[invalid_rows, column] = valid_mean

        # replace 0 values where they are not right
        elif column in zero_is_bad_value:
            df = replace_value_with_grouped_mean(df, 0, column, 'region')

        elif column in other_bad_value:
            df = replace_value_with_grouped_mean(df, -2e-8, column, 'region')

        # strings to categoricals
        elif column_type == "object":
            df.loc[:, column] = df[column].astype('category')

    return df


def replace_value_with_grouped_mean(df, value, column, to_groupby):
    """ For a given numeric value (e.g., 0) in a particular column, take the
        mean of column (excluding value) grouped by to_groupby and return that
        column with the value replaced by that mean.

        :param df: The dataframe to operate on.
        :param value: The value in column that should be replaced.
        :param column: The column in which replacements need to be made.
        :param to_groupby: Groupby this variable and take the mean of column.
                           Replace value with the group's mean.
        :returns: The data frame with the invalid values replaced
    """
    invalid_mask = (df[column] == value)

    # get the mean without the invalid value
    means_by_group = (df[~invalid_mask]
        .groupby(to_groupby)[column]
        .mean())

    # get an array of the means for all of the data
    means_array = means_by_group[df[to_groupby].values].values

    # assignt the invalid values to means
    df.loc[invalid_mask, column] = means_array[invalid_mask]

    return df
