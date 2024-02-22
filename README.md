# Document Streaming Pipeline

In this project we are building scalable end-to-end solution that captures e-commerce data  about bought items, invoices and customers, transforms it, process it , writes it to db and generates insightful visualisations. This project can be split into following tasks: 
* Preparing the data by changing the data type, filling or removing the NA cells, converting each line of dataset to json,since data will be stored as documents in db.
* Creating the API, JSON schema which describes data formats and validate JSON documents. Before API is used, it is tested. In test phase, we do not stream events therefore code to create kafka string is commented out.
* Uploading test json collection to postman, conecting to localhost and testing. 
* Adding in test streaming events service. At this point API is locally deployed while streaming event platform (kafka) is on container. Via cli we create internal ingestion topic and local consumer who reads and processes events.
* Building docker container for API and changing conection to streaming service from localhost to kafka:9092  
* Expanding docker compose file with spark  notebook, db (mongodb) and db ui (mongodb express) services. Spark notebook reads messages from event streaming platform and writes it in specific format to db. Additionaly,  we create event streaming output topic and consumer for spark job via cli. 
* Writing documents where we: 1. run our dockerized app with compose, 2. create output with json documents, 3. run spark notebook,  4. send json lines to API with input client script.
* Creating streamlit script which reads lines from db and creates visualisation on basis of data:

![alt text](https://github.com/tamaricki/document-streaming-pipeline/blob/main/streamlitapp/streamlit_screenshot.png)


### Design 

Project high-level design: 
![alt text](https://github.com/tamaricki/document-streaming-pipeline/blob/main/streamlitapp/image.png)


### Data 

For this project I used random sample of 10.000 entries about online retail transactions. Each transaction contains following info: invoice no., stock code, description, quantity, invoice date, unit price, customer id and coutry. Data is taken from e-commerce dataset on [Kaggle](https://www.kaggle.com/datasets/carrie1/ecommerce-data). 

### Used Tools 

* Data cleanup, csv to json transformation: Python, pandas
* API creation: FastAPI
* API Test: Postman 
* Message streaming: Apache Kafka 
* Applications containerized with Docker
* Reading from kafka and writing to db: pyspark jupyter notebook
* Document storage: Mongodb 
* Dashboard: streamlit 

