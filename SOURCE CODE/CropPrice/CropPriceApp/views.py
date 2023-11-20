from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
import os
from django.core.files.storage import FileSystemStorage
import pymysql
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor

global uname

le1 = LabelEncoder()

dataset = pd.read_csv("Dataset/CropDataset.csv",encoding='iso-8859-1',usecols=['variety','max_price','Rainfall'])
dataset.fillna(0, inplace = True)

def PredictCropPricesAction(request):
    if request.method == 'POST':
        item = request.POST.get('item', False)
        dataset1 = pd.read_csv("Dataset/CropDataset.csv",encoding='iso-8859-1',usecols=['variety','max_price','Rainfall','district'])
        dataset1.fillna(0, inplace = True)
        df = dataset1.loc[(dataset1['variety'] == item)]
        print(df)
        Y = df.values[:,2:3]
        district = df.values[:,0:1].ravel()
        df.drop(['max_price'], axis = 1,inplace=True)
        df.drop(['district'], axis = 1,inplace=True)
        df['variety'] = pd.Series(le1.fit_transform(df['variety'].astype(str)))
        df.fillna(0, inplace = True)
        print(Y)
        X = df.values
        sc = MinMaxScaler(feature_range = (0, 1))
        X = sc.fit_transform(X)
        Y = sc.fit_transform(Y)
        X_train = X
        Y_train = Y
        X_test = X
        Y_test = Y

        dt_regression = DecisionTreeRegressor()
        dt_regression.fit(X_train, Y_train.ravel())
        predict = dt_regression.predict(X_test)
        dt_mse = mean_squared_error(Y_test.ravel(),predict.ravel())
        dt_accuracy = 1.0 - dt_mse

        knn_regression = KNeighborsRegressor(n_neighbors=2)
        knn_regression.fit(X_train, Y_train.ravel())
        predict = knn_regression.predict(X_test)
        knn_mse = mean_squared_error(Y_test.ravel(),predict.ravel())
        knn_accuracy = 1.0 - knn_mse

        rf_regression = RandomForestRegressor()
        rf_regression.fit(X_train, Y_train.ravel())
        predict = rf_regression.predict(X_test)
        rf_mse = mean_squared_error(Y_test.ravel(),predict.ravel())
        rf_accuracy = 1.0 - rf_mse
        predict1 = predict.reshape(predict.shape[0],1)
        predict1 = sc.inverse_transform(predict1)
        predict1 = predict1.ravel()
        labels = sc.inverse_transform(Y_test)
        labels = labels.ravel()
        output = '<table border=1><tr><th><font size="" color="black">District Market</th><th><font size="" color="black">Crop Name</th><th><font size="" color="black">Original Price</th>'
        output += '<th><font size="" color="black">Predicted Price</th></tr>'
        for i in range(len(predict1)):
            output += '<tr><td><font size="" color="black">'+district[i]+'</td>'
            output += '<td><font size="" color="black">'+item+'</td>'
            output += '<td><font size="" color="black">'+str(labels[i])+'</td>'
            output += '<td><font size="" color="black">'+str(predict1[i])+'</td></tr>'
        output += '<tr><td><font size="" color="black">Random Forest Accuracy</td>'
        output += '<td><font size="" color="black">'+str(rf_accuracy)+'</td></tr>'
        output += '<tr><td><font size="" color="black">Decision Tree Accuracy</td>'
        output += '<td><font size="" color="black">'+str(dt_accuracy)+'</td></tr>'
        output += '<tr><td><font size="" color="black">KNN Accuracy</td>'
        output += '<td><font size="" color="black">'+str(knn_accuracy)+'</td></tr>'
        context= {'data':output}
        print(output)
        plt.plot(Y_test.ravel(), color = 'red', label = 'Original Price')
        plt.plot(predict.ravel(), color = 'green', label = 'Predicted Price')
        plt.title('Crop Price Forecasting')
        plt.xlabel('Current Price for Crop '+item)
        plt.ylabel('Predicted Price for Crop '+item)
        plt.legend()
        plt.show()
        return render(request, 'ViewPrices.html', context)

def PredictCropPrices(request):
    if request.method == 'GET':
        variety = np.unique(dataset['variety'])
        output = '<tr><td><font size="" color="black">Choose&nbsp;Crop&nbsp;Name</font></td><td><select name=item>'
        for i in range(len(variety)):
            output += '<option value="'+str(variety[i])+'">'+str(variety[i])+'</option>'
        output += "</select></td></tr>"
        context= {'data1':output}
        return render(request, 'PredictCropPrices.html', context)

   
def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def AdminLogin(request):
    if request.method == 'GET':
       return render(request, 'AdminLogin.html', {})

def FarmerLogin(request):
    if request.method == 'GET':
       return render(request, 'FarmerLogin.html', {})
    

def Signup(request):
    if request.method == 'GET':
       return render(request, 'Signup.html', {})

def getOutput(table,length):
    font = '<font size='' color=black>'
    output=""
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '12345', database = 'cropinfo',charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("select * from "+table)
        rows = cur.fetchall()
        for row in rows:
            output+="<tr>"
            for i in range(0,length):
                output+="<td><font size='' color=black>"+font+row[i]+"</td>"
    return output

def ViewSchemes(request):
    if request.method == 'GET':
        output = '<table border=1 align=center width=100%>'
        font = '<font size='' color=black>'
        arr = ['Scheme ID','Scheme Name','Scheme Description','Required Documents','Scheme Launch Date','Scheme End Date']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        output += getOutput("addscheme",len(arr))
        context= {'data':output}
        return render(request, 'ViewSchemes.html', context)    


def AdminLoginAction(request):
    global uname
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        if username == 'Admin' and password == 'Admin':
            uname = username
            context= {'data':'welcome '+username}
            return render(request, 'AdminScreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'ExpertLogin.html', context)
        
def FarmerLoginAction(request):
    global uname
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        index = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '12345', database = 'cropinfo',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username,password FROM signup")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and password == row[1]:
                    uname = username
                    index = 1
                    break		
        if index == 1:
            context= {'data':'welcome '+uname}
            return render(request, 'FarmerScreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'FarmerLogin.html', context)

def SignupAction(request):
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        gender = request.POST.get('t4', False)
        email = request.POST.get('t5', False)
        address = request.POST.get('t6', False)
        output = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '12345', database = 'cropinfo',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username FROM signup")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    output = username+" Username already exists"
                    break
        if output == 'none':
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '12345', database = 'cropinfo',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO signup(username,password,contact_no,gender,email,address) VALUES('"+username+"','"+password+"','"+contact+"','"+gender+"','"+email+"','"+address+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                output = 'Signup Process Completed'
        context= {'data':output}
        return render(request, 'Signup.html', context)
      


def AddScheme(request):
    if request.method == 'GET':
       return render(request, 'AddScheme.html', {})

def AddSchemeAction(request):
    if request.method == 'POST':
        sid = request.POST.get('t1', False)
        name = request.POST.get('t2', False)
        desc = request.POST.get('t3', False)
        document = request.POST.get('t4', False)
        start = request.POST.get('t5', False)
        end = request.POST.get('t6', False)
               
        output = "none"
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '12345', database = 'cropinfo',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO addscheme(scheme_id,scheme_name,description,document,start_date,end_date) VALUES('"+sid+"','"+name+"','"+desc+"','"+document+"','"+start+"','"+end+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            output = 'New Scheme details added'
        context= {'data':output}
        return render(request, 'AddScheme.html', context)

