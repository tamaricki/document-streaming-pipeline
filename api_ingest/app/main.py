
from fastapi import FastAPI, status, HTTPException

#these are needed for turning classes to jsons are return
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import json

#pydantic is used for data validation when creating json Class or schema . Data is ingested as string before writing
#is done the validation 
from pydantic import BaseModel

from datetime import datetime 
from kafka import KafkaProducer, producer

class InvoiceItem(BaseModel):
    #inovice no was int in example , and CustomerID might be also str, error on postman StockCode should be string
    InvoiceNo: str
    StockCode: str
    Description: str
    Quantity: int
    InvoiceDate: str
    UnitPrice: float
    CustomerID: int
    Country: str

app = FastAPI()

@app.get("/")
async def root():
    return {'message':'Hello World'}
 
#adding new invoice 

@app.post("/invoiceitem")
async def post_invoice_item(item: InvoiceItem): # new invoice which contains info in json format
    print('message received')

    try:
        date = datetime.strptime(item.InvoiceDate, '%m/%d/%Y %H:%M') 
        print('found a timestamp', date)

        #reformating the date 

        item.InvoiceDate = date.strftime('%d-%m-%Y %H:%M:%S')
        print('New date format', item.InvoiceDate)

        json_item = jsonable_encoder(item)

        #json as string 
        json_str = json.dumps(json_item)

        print(json_str)

        #produce string 
        produce_kafka_string(json_str)
        return JSONResponse(content = json_item, status_code=201)
    #error if datetime format does not fit 
    except ValueError:
        return JSONResponse(content = jsonable_encoder(item), status_code=400)


def produce_kafka_string(json_str):
    producer = KafkaProducer(bootstrap_servers="kafka:9092", acks=1) #for local test used localhost:9093
    #string to be written as bytes to match kafka requirements
    producer.send('ingestion-topic', bytes(json_str, 'utf-8'))
    producer.flush()
        
