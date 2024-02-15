
import json
import requests

#we will first read entire file and then send one by one line in json format 

with open('./output.txt', 'r') as f:
    data = f.readlines()

size = len(data)
#for test we can first test with smaller no of data like 15

for i in range(size):  #afterwards we can remove 
    myjson = json.loads(data[i])
    print(myjson)
    response = requests.post('http://localhost:80/invoiceitem', json=myjson)

    #for debuging 
    #print('Status code', response.status_code)
    #print(response.json())


#as alternative, we can use linecache

#import linecache
    #line =linecache.getline('../output.txt', i)
    #myjason= json.loads(line)
    #response = requests.post(....)
