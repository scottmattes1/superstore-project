import pandas as pd


################## CHECK NULLS DUPLICATES FUNCTION #################

def check_nulls_duplicates(df):
    print(f'There are {df.isnull().sum().sum()} nulls in the dataset.')
    print(f'There are {df.duplicated().sum()} duplicates in the dataset.')