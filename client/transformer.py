
#import json
import numpy as np
import pandas as pd 

#with transformer file we transform csv file to json 
df = pd.read_csv('../../data/data.csv') # small_data just small samle of 350 entries first 
                                      # data.csv whole dataset  

#add json column in df, splitlines  this splits into multiple rows 

df['json'] = df.to_json(orient='records', lines=True).splitlines()

dfjson = df['json']

#this output can be saved then in txt file , date forward with forward slash is escaped to align with json schema

np.savetxt(r'./output.txt', dfjson.values, fmt='%s')
#print(df.sample(6))