from engarde.decorators import none_missing


@none_missing()
def replace_all_nulls_with_value(df, replacement=0):
    """ toy method for testing that wraps ``DataFrame.fillna`` """
    if replacement is None:
        raise ValueError('Replacement must be a value')
    return df.fillna(replacement)
