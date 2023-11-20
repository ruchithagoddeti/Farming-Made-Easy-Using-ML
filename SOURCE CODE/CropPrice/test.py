import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt

le1 = LabelEncoder()
le2 = LabelEncoder()

dataset = pd.read_csv("Dataset/CropDataset.csv",usecols=['variety','max_price','Rainfall'])
dataset.fillna(0, inplace = True)
df = dataset.loc[(dataset['variety'] == 'Coriander Seed')]


Y = df.values[:,1:2]
df.drop(['max_price'], axis = 1,inplace=True)
df['variety'] = pd.Series(le1.fit_transform(df['variety'].astype(str)))
df.fillna(0, inplace = True)
X = df.values

sc = MinMaxScaler(feature_range = (0, 1))
X = sc.fit_transform(X)
Y = sc.fit_transform(Y)
print(X.shape)

X_train = X
Y_train = Y
X_test = X
Y_test = Y

svr_regression = RandomForestRegressor()
#training SVR with X and Y data
svr_regression.fit(X_train, Y_train.ravel())
#performing prediction on test data
predict = svr_regression.predict(X_test)
svm_mse = mean_squared_error(Y_test.ravel(),predict.ravel())
print(svm_mse)
#plotting comparison graph between original values and predicted values
plt.plot(Y_test.ravel(), color = 'red', label = 'Observed Crime Location')
plt.plot(predict.ravel(), color = 'green', label = 'Predicted Crime Location')
plt.title('SVM Crime Location Forecasting')
plt.xlabel('Original Observed Crimes Locations')
plt.ylabel('Forecasting Crimes Locations')
plt.legend()
plt.show()
print(predict)
predict = predict.reshape(predict.shape[0],1)
predict = sc.inverse_transform(predict)
predict = predict.ravel()
labels = sc.inverse_transform(Y_test)
labels = labels.ravel()

for i in range(len(labels)):
    print(str(predict[i])+" "+str(labels[i]))
