import pandas as pd
import os


class FeatureExtractor(object):
    def __init__(self):
        pass

    def fit(self, x_df, y_array):
        pass

    def transform(self, x_df):
        
        # path = os.path.dirname(__file__)  # use this in submission
        path = os.getcwd()  # use this in notebook

        # x_encoded = x_df

        x_encoded = x_df.set_index("DateOfDeparture")

        # Add temperatures.
        # -------------

        # temperatures = pd.read_csv(os.path.join(path, "Submission/temperatures.csv")).\
        #    set_index("DateOfDeparture")

        # x_encoded = pd.concat([x_encoded, temperatures], axis=1, join='inner')

        # Add baril price (on Booking).
        # -------------

        baril_price = pd.read_csv(os.path.join(path, "Submission/baril_departure.csv")).\
            set_index("DateOfDeparture")

        x_encoded = pd.concat([x_encoded, baril_price], axis=1, join='inner')

        # Add holidays.
        # -------------

        holidays = pd.read_csv(os.path.join(path, "Submission/holidays.csv")).\
            set_index("DateOfDeparture")

        x_encoded = pd.concat([x_encoded, holidays], axis=1, join='inner').reset_index()

        x_encoded = x_encoded.join(pd.get_dummies(x_encoded['Departure'], prefix='d'))
        x_encoded = x_encoded.join(pd.get_dummies(x_encoded['Arrival'], prefix='a'))
        x_encoded = x_encoded.drop('Departure', axis=1)
        x_encoded = x_encoded.drop('Arrival', axis=1)

        # following http://stackoverflow.com/questions/16453644/regression-with-date-variable-using-scikit-learn

        x_encoded['DateOfDeparture'] = pd.to_datetime(x_encoded['DateOfDeparture'])
        x_encoded['year'] = x_encoded['DateOfDeparture'].dt.year
        x_encoded['month'] = x_encoded['DateOfDeparture'].dt.month
        x_encoded['day'] = x_encoded['DateOfDeparture'].dt.day
        x_encoded['weekday'] = x_encoded['DateOfDeparture'].dt.weekday
        x_encoded['week'] = x_encoded['DateOfDeparture'].dt.week
        x_encoded['n_days'] = x_encoded['DateOfDeparture'].apply(lambda date: (date - pd.to_datetime("1970-01-01")).days)

        x_encoded = x_encoded.join(pd.get_dummies(x_encoded['year'], prefix='y'))
        x_encoded = x_encoded.join(pd.get_dummies(x_encoded['month'], prefix='m'))
        x_encoded = x_encoded.join(pd.get_dummies(x_encoded['day'], prefix='d'))
        x_encoded = x_encoded.join(pd.get_dummies(x_encoded['weekday'], prefix='wd'))
        x_encoded = x_encoded.join(pd.get_dummies(x_encoded['week'], prefix='w'))

        x_encoded = x_encoded.drop('DateOfDeparture', axis=1)
        x_array = x_encoded.values
        
        return x_array
