# Document Streaming Pipeline

In this project I built scalable end-to-end solution that captures e-commerce data  about bought items, invoices and customers, transforms it, process it , writes it to db and generates insightful visualisations. Project can be split into following tasks: 
* Preparing the data by changing the data type, filling or removing the NA cells, converting each line of dataset to json,since data will be stored as documents in database.
* Creating the API, JSON schema which describes data formats and validate JSON documents. 
* Uploading test json collection to postman, conecting to localhost and testing. 
* Expanding the test with streaming events service. At this point API is locally deployed while streaming event platform (kafka) is on container. 
* Building docker container for API and changing conection to streaming service from localhost to kafka:9092  
* Expanding docker compose file with spark  notebook, database (mongodb) and database ui (mongodb express) services. Spark notebook reads messages from event streaming platform and writes it in specific format to database. For that purpose is created event streaming output topic and consumer. 
* Writing documents is done in following steps: 1. start dockerized app with compose, 2. create json documents, 3. run spark notebook  4. send json lines to API with input client script 5. write with spark lines to database
* Creating streamlit script which reads lines from database and creates visualisation on basis of data:

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
* Reading from kafka and writing to data base: pyspark jupyter notebook
* Document storage: Mongodb 
* Dashboard: streamlit 

