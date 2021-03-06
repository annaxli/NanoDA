import numpy as np
import pandas
import scipy
import statsmodels.api as sm

"""
In this optional exercise, you should complete the function called 
predictions(turnstile_weather). This function takes in our pandas 
turnstile weather dataframe, and returns a set of predicted ridership values,
based on the other information in the dataframe.  

In exercise 3.5 we used Gradient Descent in order to compute the coefficients
theta used for the ridership prediction. Here you should attempt to implement 
another way of computing the coeffcients theta. You may also try using a reference implementation such as: 
http://statsmodels.sourceforge.net/devel/generated/statsmodels.regression.linear_model.OLS.html

One of the advantages of the statsmodels implementation is that it gives you
easy access to the values of the coefficients theta. This can help you infer relationships 
between variables in the dataset.

You may also experiment with polynomial terms as part of the input variables.  

The following links might be useful: 
http://en.wikipedia.org/wiki/Ordinary_least_squares
http://en.wikipedia.org/w/index.php?title=Linear_least_squares_(mathematics)
http://en.wikipedia.org/wiki/Polynomial_regression

This is your playground. Go wild!

How does your choice of linear regression compare to linear regression
with gradient descent computed in Exercise 3.5?

You can look at the information contained in the turnstile_weather dataframe below:
https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv

Note: due to the memory and CPU limitation of our amazon EC2 instance, we will
give you a random subset (~10%) of the data contained in turnstile_data_master_with_weather.csv

If you receive a "server has encountered an error" message, that means you are hitting 
the 30 second limit that's placed on running your program. See if you can optimize your code so it
runs faster.
"""

def predictions(weather_turnstile):


    turnstile_df = weather_turnstile
    # print prediction

    # print prediction['hour']
    features_df = pandas.DataFrame({'hour': turnstile_df['hour'], 
                                    # 'tempi': turnstile_df['tempi'], #0.462161286773
                                    # 'meantempi': turnstile_df['meantempi'], #0.462484169607
                                    # 'wspdi': turnstile_df['wspdi'], # 0.462239183279
                                    # 'meanwspdi': turnstile_df['meanwspdi'], # 0.462023237442
                                    'precipi': turnstile_df['precipi']})
    label = turnstile_df['ENTRIESn_hourly']

    normalized_features = normalize_features(features_df)

    # Adds y-intercept to model
    normalized_features = sm.add_constant(normalized_features)

    # rain acts as a dummy variable because it is categorical, therefore doesn't need normalization
    normalized_features = normalized_features.join([turnstile_df['rain']])
    
    # add dummy variables of turnstile units to features
    dummy_units = pandas.get_dummies(turnstile_df['UNIT'], prefix='unit')
    normalized_features = normalized_features.join([dummy_units])
    # add dummy variables of day week to features (day of week is categorical)
    dummy_dayweek = pandas.get_dummies(turnstile_df['day_week'], prefix='day_week')
    normalized_features = normalized_features.join([dummy_dayweek])
    
    model = sm.OLS(label,normalized_features)
    results = model.fit()
    # print results
    parameters = results.params
    print parameters
    results_summary = results.summary()

    print results_summary  

    prediction = results.predict(normalized_features)
    print prediction
    return prediction

def normalize_features(array):
    """
    Normalize the features in the data set.
    """
    array_normalized = (array-array.mean())/array.std()
    print "array.mean() ", array.mean()
    return array_normalized

def compute_r_squared(label, predictions):
    # Write a function that, given two input numpy arrays, 'data', and 'predictions,'
    # returns the coefficient of determination, R^2, for the model that produced 
    # predictions.
    # 
    # Numpy has a couple of functions -- np.mean() and np.sum() --
    # that you might find useful, but you don't have to use them.

    sum_of_data_minus_predictions = np.sum(np.square(label - predictions))
    sum_of_predictions_minus_mean = np.sum(np.square(label - np.mean(label)))
    r_squared = 1 - (sum_of_data_minus_predictions / sum_of_predictions_minus_mean)

    return r_squared

def imp():
    turnstile_df = pandas.read_csv('turnstile_weather_v2.csv')
    return turnstile_df

if __name__ == '__main__':
    data = imp()
    prediction = predictions(data)
    label = data['ENTRIESn_hourly']
    # print "data: \n",data
    # print "pred: \n",prediction
    # print "lbl: \n",label
    
    print compute_r_squared(label,prediction)
