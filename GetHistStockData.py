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
Module_Data_Path = "/Users/andrejtupikin/pythonfirststeps/GetHistStockData/Data/"

d_M_Y = "Y"
Ticks_s = "86400"
Dur = "15"
Ex = "ETR"
Data = "d,o"

def ReadMnemonicCSV():

    MnemonicData = pd.read_csv('/Users/andrejtupikin/pythonfirststeps/GetXetraMnemonic/Data/Mnemonic.csv')
    
    for x in range(0,len (MnemonicData)):

        StockDataURL = "https://www.google.com/finance/getprices?q=" + str(MnemonicData['Mnemonic'][x]) + "&x=" + Ex + "&i=" + Ticks_s + "&p=" + Dur + d_M_Y + "&f=" + Data
        
        StockDataURL_Data = requests.get(StockDataURL,headers=headers).text
        
        # write to csv
        csv_df = pd.DataFrame({str(MnemonicData['Mnemonic'][x]): StockDataURL_Data}, index=[x])
        csv_df.to_csv(Module_Data_Path + "DataGotOnDates/" + strftime("%d %b %Y", gmtime()) + "/" + Dur + d_M_Y + "_" + Ticks_s + "s/" + str(MnemonicData['Mnemonic'][x]) + '.csv', index=False)
        
        if not os.path.isfile(Module_Data_Path + "AllData/" + "/" + Dur + d_M_Y + "_" + Ticks_s + "s/" + str(MnemonicData['Mnemonic'][x]) + '.csv'):
            csv_df.to_csv(Module_Data_Path + "AllData/" + "/" + Dur + d_M_Y + "_" + Ticks_s + "s/" + str(MnemonicData['Mnemonic'][x]) + '.csv', index=False)
        
        print x, StockDataURL
        
        
def CreateFolder():
    
    if not os.path.exists(Module_Data_Path + "AllData/" + "/" + Dur + d_M_Y + "_" + Ticks_s + "s/"):
        os.makedirs(Module_Data_Path + "AllData/" + "/" + Dur + d_M_Y + "_" + Ticks_s + "s/")
    
    if not os.path.exists(Module_Data_Path + "DataGotOnDates/" + strftime("%d %b %Y", gmtime()) + "/" + Dur + d_M_Y + "_" + Ticks_s + "s/"):
        os.makedirs(Module_Data_Path + "DataGotOnDates/" + strftime("%d %b %Y", gmtime()) + "/" + Dur + d_M_Y + "_" + Ticks_s + "s/")
        

if __name__ == "__main__":
    CreateFolder()
    ReadMnemonicCSV()
    
    
    
        #print(
           #datetime.fromtimestamp(
                #int("1284101485")
            #).strftime('%Y-%m-%d %H:%M:%S')
        #)