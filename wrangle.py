import pandas as pd
import os
import sys
from sklearn.model_selection import train_test_split


import env

################## NORMALIZE COLUMN NAMES FUNCTION ###################

def normalize_column_names(df):
    """
    Takes in a dataframe and iterates through the columns, puts them in a lower case, and replaces separating characters and whitespace with an underscore. Returns the dataframe with the normalized column names
    """
    for col in df.columns:
        new_col = col.strip().lower()  # Clean and standardize the column name
        for char in [' ', '.', '-', ',', '+']:
            new_col = new_col.replace(char, '_')  # Replace specific characters with underscores
        df = df.rename(columns={col: new_col})  # Rename the column with the cleaned and standardized name
    return df


########################## DATE SET INDEX FUNCTION #########################
    
def date_set_index(df, col):
    """
    Renames the date column to 'date' and sets it as the index of the dataframe. Returns the updated dataframe.
    """
    # Rename the designated columns 'date'
    df = df.rename(columns={col: 'date'})
    
    # Casts the date column to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Set the date as the index
    df = df.set_index('date')

    return df


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
    df = normalize_column_names(df)
    df = df[['customer_id', 'order_date', 'segment', 'state', 'region', 'product_id', 'category', 'sales', 'quantity', 'discount', 'profit']]
    df = date_set_index(df, 'order_date')
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
    dummies = normalize_column_names(dummies)
    
    return dummies
