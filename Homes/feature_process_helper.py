import timeit
import pandas as pd
import numpy as np

def mssubclass(train, test):
    for i in (train, test):
        i['MSSubClass'] = i['MSSubClass'].apply(lambda x: str(x))
    return train, test

def lotfrontage(train, test):
    for i in (train, test):
        i['LotFrontage'] = i['LotFrontage'].fillna(train['LotFrontage'].mean())
    return train, test

def garageyrblt(train, test):
    for i in (train, test):
        i['GarageYrBlt'] = i['GarageYrBlt'].fillna(train['GarageYrBlt'].mean())
    return train, test

def impute(train, test):
    for i in (train, test):
        for s in ['LotFrontage', 'LotArea', 'MasVnrArea', 'BsmtFinSF1', 
                              'BsmtFinSF2', '1stFlrSF', '2ndFlrSF', 'LowQualFinSF', 
                              'GrLivArea', 'OpenPorchSF', 'EnclosedPorch', '3SsnPorch', 
                              'ScreenPorch', 'PoolArea', 'BsmtUnfSF', 'TotalBsmtSF', 
                              'BsmtFullBath', 'BsmtHalfBath', 'GarageCars', 'GarageArea']:
            i[s] = i[s].fillna(0)
    return train, test

from sklearn.preprocessing import StandardScaler

def scale(train, test, cols = ['LotFrontage', 'LotArea', 'MasVnrArea', 'BsmtFinSF1', 
                              'BsmtFinSF2', '1stFlrSF', '2ndFlrSF', 'LowQualFinSF', 
                              'GrLivArea', 'OpenPorchSF', 'EnclosedPorch', '3SsnPorch', 
                              'ScreenPorch', 'PoolArea']):
    for i in cols:
        sc = StandardScaler()
        train[i] = sc.fit_transform(train[i].reshape(-1,1))
        test[i] = sc.transform(test[i].reshape(-1,1))
    return train, test

def dummies(train, test):
    start = timeit.default_timer()
    columns = [i for i in train.columns if type(train[i].iloc[1]) == str or type(train[i].iloc[1]) == float]
    for column in columns:
        train[column].fillna('NULL', inplace = True)
        good_cols = [column+'_'+i for i in train[column].unique()[1:] if i in test[column].unique()]
        train = pd.concat((train, pd.get_dummies(train[column], prefix = column)[good_cols]), axis = 1)
        test = pd.concat((test, pd.get_dummies(test[column], prefix = column)[good_cols]), axis = 1)
        del train[column]
        del test[column]
    print timeit.default_timer() - start, 'seconds'
    return train, test

def log(train, test, y):
    for i in (train, test):
		#log transform skewed numeric features:
		numeric_feats = train.dtypes[all_data.dtypes != "object"].index

		skewed_feats = train[numeric_feats].apply(lambda x: skew(x.dropna())) #compute skewness
		skewed_feats = skewed_feats[skewed_feats > 0.75]
		skewed_feats = skewed_feats.index

		all_data[skewed_feats] = np.log1p(all_data[skewed_feats])

    y = np.log1p(y)
    return train, test, y