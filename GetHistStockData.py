import urllib
import requests
import time, threading, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mt
import json
import os
import regex as re
from googlefinance import getQuotes
from datetime import datetime
from time import gmtime, strftime

headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}

def ReadMnemonicCSV():

    MnemonicData = pd.read_csv('/Users/andrejtupikin/pythonfirststeps/GetXetraMnemonic/Data/Mnemonic.csv')
    
    StockDataURL_Data = ["" for y in range(0,len (MnemonicData))]
    
    for x in range(0,len (MnemonicData)):

        StockDataURL = "https://www.google.com/finance/getprices?q=" + str(MnemonicData['Mnemonic'][x]) + "&x=ETR&i=60&p=10d&f=d,c,h,l,o,v"
        
        StockDataURL_Data[x] = requests.get(StockDataURL,headers=headers).text
        
        csv_df = pd.DataFrame({str(MnemonicData['Mnemonic'][x]): StockDataURL_Data})
        csv_df.to_csv("/Users/andrejtupikin/pythonfirststeps/GetHistStockData/Data/" + str(MnemonicData['Mnemonic'][x]) + '.csv', index=False)
        
        print x, StockDataURL

if __name__ == "__main__":
    
    ReadMnemonicCSV()
    
    