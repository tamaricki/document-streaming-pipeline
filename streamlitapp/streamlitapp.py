
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

st.set_page_config(page_title='Customer Information', layout='wide', initial_sidebar_state='expanded')

#we create data frame from db collection 
df = pd.DataFrame(list(mycol.find())) 

df = df[df['CustomerID']!='0'] # exclude customers without customerID
#extract date from datetime and keep datetime64 format 
df['InvoiceDate']= pd.to_datetime(df['InvoiceDate'], dayfirst=True).dt.normalize()   
#change datatype in order to create visualisations, calculate total value , extract month 
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
transactions = df.groupby('Month')['StockCode'].count().reset_index(name='TransactionsCount')


#%%
# we can create drop down list of cucstomer Ids for selection 
unique_customers = df['CustomerID'].unique()

cust_id = st.sidebar.selectbox("Select the Customer ID", unique_customers)

customer_invoices = df[df['CustomerID']==cust_id]['InvoiceNo']

inv_no = st.sidebar.selectbox("Select invoice", customer_invoices)


#%%
#adding sections for visualisations
#st.markdown('---')
cols = st.columns((4.0, 4.0), gap='medium')

with cols[0]:
    st.markdown("#### Output Customer Invoices")
    if cust_id:
        my_query = {"CustomerID": cust_id}
    #zeros for columns in table which we do not want to see in results 
        mydoc = mycol.find(my_query, {'_id':0, 'StockCode':0, 'Description':0, 'Quantity': 0, 'Country':0, 'UnitPrice':0})

        df_cust = pd.DataFrame(mydoc)

        df_cust.drop_duplicates(subset='InvoiceNo', keep='first', inplace=True)

        table = st.dataframe(data=df_cust)
    if inv_no:
        my_query = {"InvoiceNo": inv_no}
        result = mycol.find(my_query, {"_id":0, "InvoiceDate": 0, "Country": 0, "CustomerID": 0})

        df_inv = pd.DataFrame(result)
    
        reindex =df_inv.reindex(sorted(df_inv.columns), axis=1)

        st.header("Output by Invoice number")
  
        table = st.dataframe(data=reindex)

    custom_df = df[df['CustomerID']==cust_id][['Month', 'TotalValue']]
    new_df = custom_df.groupby('Month')['TotalValue'].sum().reset_index().sort_values(by=['Month'])

    #fig=plt.figure(figsize=(6,4))
    #plt.bar(new_df['Month'], new_df['TotalValue'], label='Purchases for customer {}'.format(cust_id), color='slategrey')
    #plt.xlabel('Month')
    #plt.ylabel('Value')
    #plt.legend()
    #plt.axis('tight')
    #st.pyplot(fig)

    st.bar_chart(new_df, x='Month', y='TotalValue')

    counts = df.UnitPrice.value_counts().reset_index(name='counts')
    #fit=plt.figure()
    st.bar_chart(counts, x='UnitPrice', y='counts')
   # plt.legend()
    #plt.xlim(0,20)
    #st.pyplot(fit)

    
    

with cols[1]:

    st.write('#### Data Analysis')

    fig = plt.figure()
    plt.barh(dec_best['CustomerID'].head(10), dec_best['total_value'].head(10), color = 'lightgreen')
    plt.xlabel('Total Value Purchased')
    plt.ylabel('Customer ID')
    plt.xticks(rotation=45)
    plt.title('Top 10 Customers Purchases December')
    st.pyplot(fig)

    fig = plt.figure()
    plt.bar(transactions['Month'], transactions['TransactionsCount'], color='slateblue')
    plt.xlabel('Month')
    #plt.xticks(rotation=45)
    plt.title('Transactions Count per Month')
    st.pyplot(fig)


    #fig= plt.figure()
    #plt.barh(jul_best['CustomerID'].head(10), jul_best['total_value'].head(10), color='thistle' )
    #plt.xlabel('Total Value Purchased')
    #plt.xticks(rotation=45)
    #plt.ylabel('Customer ID')
    #plt.title('Top 10 Customers July')
    #st.pyplot(fig)




#%%

df.hist('UnitPrice')
plt.xlim(0,20)
plt.show()

# %%


# %%

# %%
