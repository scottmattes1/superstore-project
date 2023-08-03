import pandas as pd
import matplotlib.pyplot as plt
import wrangle
import statsmodels.api as sm
from scipy.stats import pearsonr


################## CHECK NULLS DUPLICATES FUNCTION #################

def check_nulls_duplicates(df):
    print(f'There are {df.isnull().sum().sum()} nulls in the dataset.')
    print(f'There are {df.duplicated().sum()} duplicates in the dataset.')
    
    
################### TIME WRANGLE SUPERSTORE FUNCTION #################

def time_wrangle_superstore(df, title):
    '''
    wrangles the superstore data, resamples to daily, handles the outliers, splits the data into train, validate, and test, then prints the shapes of the resulting dataframes
    '''
    
    # Bring in the data
    df = wrangle.wrangle_superstore()
    
    # Resamples the data to a daily timescale
    df = df.resample("d").sales.agg('sum')
    
    # Take measurements and assign index values to split the dataset on
    train_size = int(len(df) * .8)
    validate_size = int(len(df) * .1)
    test_size = int(len(df) - train_size - validate_size)
    validate_end_index = train_size + validate_size
    
    # Handle outliers
    df.loc[pd.to_datetime('2014-03-18')] = 7_000
    df.loc[pd.to_datetime('2016-10-02')] = 11_000
    df.loc[pd.to_datetime('2017-10-22')] = 14_000
    df.loc[pd.to_datetime('2017-03-23')] = 6_000
    df.loc[pd.to_datetime('2014-09-08')] = 10_000

    # split into train, validation, test (70/15/15)
    train = pd.DataFrame(df[: train_size])
    validate = pd.DataFrame(df[train_size : validate_end_index])
    test = pd.DataFrame(df[validate_end_index : ])
    
    print(f'''
train length: {train.shape[0]}
validate length: {validate.shape[0]}
test length: {test.shape[0]}
    ''')
    
    # Plot the dataframes
    plt.figure(figsize = (12,4))
    plt.plot(train.index, train.sales)
    plt.plot(validate.index, validate.sales)
    plt.plot(test.index, test.sales)
    plt.title(title)
    plt.xticks(rotation=90)
    plt.grid(axis='y')
    plt.show()
    
    return train, validate, test


################### MONTHLY RESAMPLE FUNCTON ###################

def weekly_resample(train, validate, test):
    '''
    Takes in train, validate, and test resamples them to a weekly timescale, and then graphs them, also prints the lengths
    '''
    
    # Resamples train, validate, and test to a weekly timescale
    train = train.resample("W").agg('sum')
    validate = validate.resample("W").agg('sum')
    test = test.resample("W").agg('sum')
    
    # Plot the dataframes
    plt.figure(figsize = (12,4))
    plt.plot(train.index, train.sales)
    plt.plot(validate.index, validate.sales)
    plt.plot(test.index, test.sales)
    plt.title('Weekly resampled sales data')
    plt.xticks(rotation=90)
    plt.grid(axis='y')
    plt.show()
    
    # Print the shape of the resulting dataframes
    print(f'''
train length: {train.shape[0]}
validate length: {validate.shape[0]}
test length: {test.shape[0]}
    ''')
        
    return train, validate, test


################# SEASONAL DECOMPOSITION FUNCTION ################

def seasonal_decomposition(train):
    '''
    Takes in the train dataframe and performs seasonal decomposition on the time-series data
    '''
    
    # Resample 'train' to weekly data and calculate the mean
    weekly_mean = train.sales.resample('W').mean()

    # Perform seasonal decomposition
    decomposition = sm.tsa.seasonal_decompose(weekly_mean)

    # Plot each component separately
    decomposition.plot()
    
    
################## PLOT AUTOCORRELATION FUNCTION ##################

def plot_autocorrelation(train):
    '''
    takes in the train data and plots the autocorrelation
    '''
    plt.figure(figsize = (12,4))
    pd.plotting.autocorrelation_plot(train.sales);
    plt.title('The autocorrelation of weekly sales data');


####################

# Stats test the days around 1 day ago for autocorrelation

def test_lag_values(train):
    '''
    takes in train and pearson's r tests shifted columns after it drops the nulls created by each shift in the for-loop. Displays the r and p-values of each lag value's correlation to the sales column
    '''
    results_list = []

    for i in range(50, 55):
        pearson = train.copy()  # Make a copy of 'train' DataFrame
        pearson[f'lag_{i}'] = pearson.sales.shift(i)
        pearson = pearson.dropna()
        r, p = pearsonr(pearson.sales, pearson[f'lag_{i}'])
        results_list.append({
            'lag': i,
            'R value': r,
            'P-value': p
        })

    results_df = pd.DataFrame(results_list)
    display(results_df)



################### TIME WRANGLE SUPERSTORE W LAG FUNCTION #################

def time_wrangle_superstore_w_lag():
    '''
    wrangles the superstore data, resamples to daily, handles the outliers, splits the data into train, validate, and test, then prints the shapes of the resulting dataframes
    '''
    
    # Bring in the data
    df = wrangle.wrangle_superstore()
    
    # Resamples the data to a daily timescale
    df = pd.DataFrame(df.resample("d").sales.agg('sum'))
    
    # Handle outliers
    df.loc[pd.to_datetime('2014-03-18')] = 7_000
    df.loc[pd.to_datetime('2016-10-02')] = 11_000
    df.loc[pd.to_datetime('2017-10-22')] = 14_000
    df.loc[pd.to_datetime('2017-03-23')] = 6_000
    df.loc[pd.to_datetime('2014-09-08')] = 10_000

    # Resample to weekly
    df = pd.DataFrame(df.resample("W").agg("sum"))
    df['lag_53'] = df.sales.shift(53)
    df = df.dropna()
    
    # Take measurements and assign index values to split the dataset on
    train_size = int(len(df) * .8)
    validate_size = int(len(df) * .1)
    test_size = int(len(df) - train_size - validate_size)
    validate_end_index = train_size + validate_size
    
    # split into train, validation, test (70/15/15)
    train = pd.DataFrame(df[: train_size])
    validate = pd.DataFrame(df[train_size : validate_end_index])
    test = pd.DataFrame(df[validate_end_index : ])
    
    print(f'''
train length: {train.shape[0]}
validate length: {validate.shape[0]}
test length: {test.shape[0]}
    ''')
    
    # Plot the dataframes
    plt.figure(figsize = (12,4))
    plt.plot(train.index, train.sales)
    plt.plot(validate.index, validate.sales)
    plt.plot(test.index, test.sales)
    plt.title("Weekly sampled sales data adjusted for 53 week lag")
    plt.xticks(rotation=90)
    plt.grid(axis='y')
    plt.show()
    
    return train, validate, test
    
    