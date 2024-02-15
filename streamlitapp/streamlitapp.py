
import streamlit as st
import pandas as pd 
import numpy as np

import pymongo

#connection to db 
myclient = pymongo.MongoClient("mongodb://localhost:27017", username='root', passwordd='example')
mydb = myclient["docstreaming"] #db name
mycol = mydb['invoices'] #collection name 

cust_id = st.sidebar.text_input("Customer ID")

if cust_id:
    my_query = {"CustomerID": cust_id}
    #zeros for columns in table which we do not want to see in results 
    mydoc = mycol.find(my_query, {'_id':0, 'StockCode':0, 'Description':0, 'Quantity': 0, 'Country':0, 'UnitPrice':0})

    df = pd.DataFrame(mydoc)

    df.drop_duplicates(subset='InvoiceNo', keep='first', inplace=True)

    st.header("Output Customer Invoices")
    table = st.dataframe(data=df)

inv_no = st.sidebar.text_input('InvoiceNo:')

if inv_no:
    my_query = {"InvoiceNo": inv_no}
    result = mycol.find(my_query, {"_id":0, "InvoiceDate": 0, "Country": 0, "CustomerID": 0})

    df = pd.DataFrame(result)
    
    reindex =df.reindex(sorted(df.columns), axis=1)

    st.header("Output by Invoice number")
    table = st.dataframe(data=reindex)