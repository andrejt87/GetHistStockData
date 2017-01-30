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
url = "http://www.xetra.com/xetra-de/instrumente/aktien/liste-der-handelbaren-aktien/xetra/1571850!search?state=H4sIAAAAAAAAADWKsQoCMRAFf0W2TqFtPsDKIuBhH5IXDawJ7m6Q47h_9xDSzTCzUY6Gq_Q3-TaY3d-XPq3EBFPy235wFbUbzCAzv6ppgIT4BPnL2VFtiUfGvRp0Tr3xGnIhXyIrHH0GZCVP5Eigg-1R8Z2zdrGj6VKNcYqaaP8BsKzzjqQAAAA&sort=sTitle+asc&hitsPerPage=50"

    
def Get_NoOfPages():
    
    source_txt = requests.get(url,headers=headers).text
    
    str_found = [m.start() for m in re.finditer('name="pageNum" type="submit">', source_txt)]
    no_str_found = len(str_found)

    NoOfPages = 0
    
    for x in range(0,no_str_found):
        
        temp_str = source_txt[str_found[x]:-1]
        
        if int(temp_str[temp_str.find(">")+1:temp_str.find("<")]) > NoOfPages:
            
            NoOfPages = int(temp_str[temp_str.find(">")+1:temp_str.find("<")])
            
    return NoOfPages
    
    
def GetNumberURLs(NoOfPages):
    
    NumberURLs = ["" for x in range(NoOfPages)]
    
    for x in range(0, NoOfPages):

       NumberURLs[x] = url + "&pageNum=" + str(x)
       
    return NumberURLs
    
    
def GetSymbolURLs(NumberURLs):
    
    SymbolURLs = [""]
    
    for x in range(0,len(NumberURLs)):
    
        source_txt = requests.get(NumberURLs[x],headers=headers).text
    
        str_found = [m.start() for m in re.finditer('!tradable', source_txt)]
        no_str_found = len(str_found)
        
        TempStr = ["" for y in range(no_str_found)]
        
        for y in range(0,no_str_found):
        
            TempStr[y] = "http://www.xetra.com/xetra-de/instrumente/aktien/liste-der-handelbaren-aktien/xetra/" + source_txt[str_found[y]-7:str_found[y]] + "!tradable"
        
        if x == 0:
            
            SymbolURLs = TempStr
            
        else:
            
            SymbolURLs = np.append(SymbolURLs,TempStr)
    
    
    return SymbolURLs
    

def GetMnemonicSymbols(SymbolURLs):
    
    MnemonicSymbols = ["" for y in range(len(SymbolURLs))]
    
    for x in range(0,len(SymbolURLs)):
        
        source_txt = requests.get(SymbolURLs[x],headers=headers).text
    
        TempStrBegin = source_txt.find("rzel")
        source_txt = source_txt[TempStrBegin:-1]
        TempStrEnd = source_txt.find("</dd>")

        MnemonicSymbols[x] = source_txt[17:TempStrEnd]
        
        csv_df = pd.DataFrame({'Mnemonic': MnemonicSymbols})
        csv_df.to_csv("/Users/andrejtupikin/pythonfirststeps/GetXetraMnemonic/Data/" + "Mnemonic" + '.csv', index=False)
        print x, MnemonicSymbols[x]
    
    return MnemonicSymbols
        
    #print MnemonicSymbols
    
    #https://www.google.com/finance/getprices?q=LHA&x=ETR&i=60&p=10d&f=d,c,h,l,o,v

if __name__ == "__main__":
    
    NoOfPages = Get_NoOfPages() 
    NumberURLs = GetNumberURLs(NoOfPages) 
    SymbolURLs = GetSymbolURLs(NumberURLs)
    GetMnemonicSymbols(SymbolURLs)
    
    