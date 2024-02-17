

import numpy as np
import pandas as pd 

#with transformer file we transform csv file to json 
#This is just a sample of 10k data 
df = pd.read_csv('../project_data.csv')
df.info()


#df.isna().sum()
df['CustomerID'].fillna(0, inplace=True)
df.isna().sum()


df['CustomerID'] = df['CustomerID'].astype('int32')




#add json column in df, splitlines  this splits into multiple rows 
df['json'] = df.to_json(orient='records', lines=True).splitlines()

dfjson = df['json']

#this output can be saved then in txt file , date forward with forward slash is escaped to align with json schema

np.savetxt(r'./output.txt', dfjson.values, fmt='%s')
#print(df.sample(6))



