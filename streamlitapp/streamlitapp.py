
import streamlit as st
import pandas as pd 
import numpy as np

import pymongo

#connection to db 
myclient = pymongo.MongoClient("mongodb://localhost:27017", username='root', passwordd='example')
mydb = myclient["docstreaming"] 


