import pandas as pd
import os
import sys
from sklearn.model_selection import train_test_split


home_directory_path = os.path.expanduser('~')
sys.path.append(home_directory_path +'/utils')

import wrangle_utils as w
import explore_utils as e
import model_utils as m
import env


####################### ACQUIRE SUPERSTORE FUNCTION ##################

def acquire_superstore():
    ''' This function checks to see if superstore.csv dataset exists, and if not, prints the link to where it can be downloaded from kaggle.'''
    filename = 'superstore.csv'

    if os.path.isfile(filename):
        df = pd.read_csv(filename, encoding='latin-1')
        return df

    else:
        print('File does not exist. Download from https://www.kaggle.com/datasets/vivek468/superstore-dataset-final/download?datasetVersionNumber=1')
        
####################### PREP SUPERSTORE FUNCTION ##################
        
def prep_superstore(df):
    """
    Takes in the acquired dataframe, normalizes the column names, keeps the most useful columns, sets the order date as the time index, sorts the index, and outputs the prepared dataframe
    """
    df = w.normalize_column_names(df)
    df = df[['customer_id', 'order_date', 'segment', 'state', 'region', 'product_id', 'category', 'sales', 'quantity', 'discount', 'profit']]
    df = w.date_set_index(df, 'order_date')
    df = df.sort_index()
    df.loc[pd.to_datetime('2014-03-18')][0] = 7_000
    df.loc[pd.to_datetime('2016-10-02')][0] = 11_000
    df.loc[pd.to_datetime('2017-10-22')][0] = 14_000
    df.loc[pd.to_datetime('2017-03-23')][0] = 6_000
    df.loc[pd.to_datetime('2014-09-08')][0] = 10_000

    return df
    
####################### WRANGLE SUPERSTORE FUNCTION ##################

def wrangle_superstore():
    df = prep_superstore(acquire_superstore())
    return df

######################## SPLIT SUPERSTORE ##########################

def split_superstore(df):
    """
    Takes in the dataframe, performs a 70/15/15 split and outputs the resulting shapes and a tuple of the train, validate, and test dataframes
    """
    train_val, test = train_test_split(df, test_size=.15)
    train, validate = train_test_split(train_val, test_size=.177)
    print(f' Train shape: {train.shape}')
    print(f' Validate shape: {validate.shape}')
    print(f' Test shape {test.shape}')
    
    return train, validate, test

######################## MAKE DUMMY COLUMNS ########################

def make_dummy_columns(df):
    category = pd.get_dummies(df.category, drop_first=True)
    region = pd.get_dummies(df.region, drop_first=True)
    segment = pd.get_dummies(df.segment, drop_first=True)
    region = pd.get_dummies(df.region, drop_first=True)

    dummies = pd.concat([category, region, segment], axis=1)
    dummies = w.normalize_column_names(dummies)
    
    return dummies
