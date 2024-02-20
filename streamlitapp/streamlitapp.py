
#%%
import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

import pymongo

#connection to db 
myclient = pymongo.MongoClient("mongodb://localhost:27017", username='root', password='example')
mydb = myclient["docstreaming"] #db name
mycol = mydb['invoices'] #collection name 



#we create data frame from db collection 
df = pd.DataFrame(list(mycol.find())) 

df = df[df['CustomerID']!='0'] # exclude customers without customerID

df['InvoiceDate']= pd.to_datetime(df['InvoiceDate']).dt.normalize()   
#df['Date'] = df['InvoiceDate'].dt.normalize()
df['Quantity'] = df['Quantity'].astype('int')
df['UnitPrice'] = df['UnitPrice'].astype('float')
df['TotalValue'] = df['UnitPrice'] * df['Quantity']
df['Month'] = df['InvoiceDate'].dt.month

#df.info()


bydate = df.groupby(['Month', 'CustomerID'])['TotalValue'].sum().reset_index(name='total_value').sort_values(by=['Month', 'total_value'], ascending=False)

jan_best = bydate[bydate['Month']==1].sort_values(by=['total_value'], ascending=False)



dec_best=bydate[bydate['Month']==12].sort_values(by=['total_value'], ascending=False)
#dec_best

nov_best=bydate[bydate['Month']==11].sort_values(by=['total_value'], ascending=False)

jul_best=bydate[bydate['Month']==7].sort_values(by=['total_value'], ascending=False)



customer = df.groupby('CustomerID')['TotalValue'].sum().sort_values(ascending=False)

#customer



#%%
# we can create drop down list of cucstomer Ids for selection 
unique_customers = df['CustomerID'].unique()


cust_id = st.sidebar.selectbox("Select the Customer ID", unique_customers)

if cust_id:
    my_query = {"CustomerID": cust_id}
    #zeros for columns in table which we do not want to see in results 
    mydoc = mycol.find(my_query, {'_id':0, 'StockCode':0, 'Description':0, 'Quantity': 0, 'Country':0, 'UnitPrice':0})

    df = pd.DataFrame(mydoc)

    df.drop_duplicates(subset='InvoiceNo', keep='first', inplace=True)

    st.header("Output Customer Invoices")
    table = st.dataframe(data=df)

customer_invoices = df[df['CustomerID']==cust_id]['InvoiceNo']

inv_no = st.sidebar.selectbox("Select invoice", customer_invoices)

if inv_no:
    my_query = {"InvoiceNo": inv_no}
    result = mycol.find(my_query, {"_id":0, "InvoiceDate": 0, "Country": 0, "CustomerID": 0})

    df = pd.DataFrame(result)
    
    reindex =df.reindex(sorted(df.columns), axis=1)

    st.header("Output by Invoice number")
  
    table = st.dataframe(data=reindex)
#%%
#adding sections for visualisations
st.markdown('---')

st.write('### Top 10 Customers for January, July and December')

fig = plt.figure()
plt.bar(jan_best['CustomerID'].head(10), jan_best['total_value'].head(10), color='slateblue')
plt.xlabel('CustomerId')
plt.ylabel('Value Purchased')
plt.xticks(rotation=45)
plt.title('Top 10 Customers in January')
st.pyplot(fig)


fig= plt.figure()
plt.barh(jul_best['CustomerID'].head(10), jul_best['total_value'].head(10), color='thistle' )
plt.xlabel('Total Value Purchased')
plt.xticks(rotation=45)
plt.ylabel('Customer ID')
plt.title('Top 10 Customers July')
st.pyplot(fig)

fig = plt.figure()
plt.barh(dec_best['CustomerID'].head(10), dec_best['total_value'].head(10), color = 'purple')
plt.xlabel('Total Value Purchased')
plt.ylabel('Customer ID')
plt.xticks(rotation=45)
plt.title('Top 10 Customers December')
st.pyplot(fig)



