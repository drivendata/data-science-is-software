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
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.grid_search import GridSearchCV


def logistic(df):
    """ Trains a multinomial logistic regression model to predict the
        status of a water pump given characteristics about the pump.

        :param df: The dataframe with the features and the label.
        :returns: A trained sklearn classifier
    """
    y = df['status_group']
    X = pd.get_dummies(df.drop('status_group', axis=1))

    lr = LogisticRegression()
    params = {'C': [0.1, 1, 10]}

    clf = GridSearchCV(lr, params, cv=3)

    return clf.fit(X, y)
