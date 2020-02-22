###############################################################################
###############################################################################
##                                       ######################################
##                                       ######################################
##           KEVIN CROSWHITE             ######################################
##                                       ######################################
##                                       ######################################
##  UNIVERSITY OF WISCONSIN - MILWAUKEE  ######################################
##        ECONOMICS MA PROGRAM           ######################################
##       KEVIN.CROSWHITE@GMAIL.COM       ######################################
##          February 22, 2020            ######################################
##      MILWAUKEE, WISCONSIN, US         ######################################
##                                       ######################################
##                                       ######################################
###############################################################################
###############################################################################




###############################################################################
###############################################################################
############################### Libraries #####################################

import pandas as pd
from bs4 import BeautifulSoup
import urllib.request as ur
import datetime
import numpy as np

###############################################################################
###############################################################################
################################# INPUTS ######################################

SPX = pd.read_csv("/Users/kevin/Documents/Datasets/SP500.csv")
SPX = list(SPX.iloc[:,0])


tickers = SPX
risk_free_rate = .021
expected_return = .08
export_statements = False
export_statement_path = "/Users/kevin/Documents/FinancialStatements/"
tax_rate = .21

###############################################################################
###############################################################################
###############################################################################


###############################################################################
########################### Table of Contents #################################
###############################################################################
##
## Scrape, format, store, and export financial statements ..............28
#### Income Statments ..................................................44
#### Cash Flows ........................................................87
#### Balance Sheets ....................................................123
##
## Scrape and Store Betas...............................................185
##
## Calculate Cost of Equity ............................................246
##
## Calculate Cost of Debt ..............................................263
##
## Calculate Debt and Equity Weights ...................................290
##
## Calculate WACC ......................................................313
##
## Calculate ROIC ......................................................328
##
## Calculate EVA .......................................................342
##
###############################################################################
###############################################################################



###############################################################################
########### Scrape, format, store, and export financial statements #############
###############################################################################

print("---- Scrape, format, store, and export financial statements ----")

income_statements = {}
balance_sheets = {}
cash_flows = {}


for index,ticker in enumerate(tickers):
    
    print("---------- " + str(ticker) + " ------------")

    # Create URLs
    url_is = "https://finance.yahoo.com/quote/" + ticker + "/financials?p=" + ticker
    url_bs = "https://finance.yahoo.com/quote/" + ticker + "/balance-sheet?p=" + ticker
    url_cf = "https://finance.yahoo.com/quote/" + ticker + "/cash-flow?p="+ ticker
    
    
##### Income Statements    
    
    # Read URLs
    read_data_income_statement = ur.urlopen(url_is).read() 
    soup_is = BeautifulSoup(read_data_income_statement,"lxml")
    print(ticker + " - Income Statement")

    # Assess how many years are posted to Yahoo Finance
    ls= [] 
    for l in soup_is.find_all("div"):          
        #Find all data structure that is ‘div’
        ls.append(l.string) # add each element one by one to the list
        ls = [e for e in ls if e not in ("Operating Expenses","Non-recurring Events")] # Exclude those columns
        new_ls = list(filter(None,ls))
        new_ls = new_ls[12:]  
        new_ls = [x.replace(",", "") for x in new_ls]
  
    if str(datetime.date.today().year - 1) in new_ls[2]:
        x = 6
    else:
        x = 5

    ls= [] 
    for l in soup_is.find_all("div"): 
        
        #Find all data structure that is ‘div’
        ls.append(l.string) # add each element one by one to the list
        ls = [e for e in ls if e not in ("Operating Expenses","Non-recurring Events")] # Exclude those columns
        new_ls = list(filter(None,ls))
        new_ls = new_ls[12:]
        new_ls = [x.replace(",", "") for x in new_ls]
        is_data = list(zip(*[iter(new_ls)]*x))
        income_statements[ticker] = pd.DataFrame(is_data[0:])
        income_statements[ticker].iloc[1:,1:] = (income_statements[ticker].iloc[1:,1:].apply(pd.to_numeric,errors="coerce") * 1000)
        
    read_data_cash_flow = ur.urlopen(url_cf).read() 
    soup_cf = BeautifulSoup(read_data_cash_flow,"lxml")
    print(ticker + " - Cash Flow")



####### Cash Flow

    # Assess how many years are posted to Yahoo Finance
    ls= [] 
    for l in soup_cf.find_all("div"):          
        #Find all data structure that is ‘div’
        ls.append(l.string) # add each element one by one to the list
        ls = [e for e in ls if e not in ("Operating Expenses","Non-recurring Events")] # Exclude those columns
        new_ls = list(filter(None,ls))
        new_ls = new_ls[12:]  
        new_ls = [x.replace(",", "") for x in new_ls]
  
    if str(datetime.date.today().year - 1) in new_ls[2]:
        x = 6
    else:
        x = 5
        
    ls= [] 
    for l in soup_cf.find_all("div"): 
        
        #Find all data structure that is ‘div’
        ls.append(l.string) # add each element one by one to the list
        ls = [e for e in ls if e not in ("Operating Expenses","Non-recurring Events")] # Exclude those columns
        new_ls = list(filter(None,ls))
        new_ls = new_ls[12:]
        new_ls = [x.replace(",", "") for x in new_ls]
        
        is_data = list(zip(*[iter(new_ls)]*x))
        cash_flows[ticker] = pd.DataFrame(is_data[0:]) 
        cash_flows[ticker].iloc[1:,1:] = (cash_flows[ticker].iloc[1:,1:].apply(pd.to_numeric,errors="coerce")*1000)


###### Balance Sheet        
        
    read_data_balance_sheet = ur.urlopen(url_bs).read() 
    soup_bs = BeautifulSoup(read_data_balance_sheet,"lxml")
    print(ticker + " - Balance Sheet")
    

    # Assess how many years are posted to Yahoo Finance
    ls= [] 
    for l in soup_bs.find_all("div"):          
        #Find all data structure that is ‘div’
        ls.append(l.string) # add each element one by one to the list
        ls = [e for e in ls if e not in ("Operating Expenses","Non-recurring Events")] # Exclude those columns
        new_ls = list(filter(None,ls))
        new_ls = new_ls[12:]  
        new_ls = [x.replace(",", "") for x in new_ls]
  
    if str(datetime.date.today().year - 1) in new_ls[1]:
        x = 5
    else:
        x = 4   

    ls = []
    for l in soup_bs.find_all("div"): 
        
        #Find all data structure that is ‘div’
        ls.append(l.string) # add each element one by one to the list
        ls = [e for e in ls if e not in ("Operating Expenses","Non-recurring Events")] # Exclude those columns
        new_ls = list(filter(None,ls))
        new_ls = new_ls[12:]
        new_ls = [x.replace(",", "") for x in new_ls]
        is_data = list(zip(*[iter(new_ls)]*x))
        balance_sheets[ticker] = pd.DataFrame(is_data[0:])
        balance_sheets[ticker].iloc[1:,1:] = (balance_sheets[ticker].iloc[1:,1:].apply(pd.to_numeric,errors="coerce")*1000)
        
        
    # Index and name columns of statements    
    income_statements[ticker] = income_statements[ticker].rename(columns=income_statements[ticker].iloc[0,:], index=income_statements[ticker].iloc[:,0])
    income_statements[ticker] = income_statements[ticker].drop(columns='Annual',index='Annual')
    cash_flows[ticker] = cash_flows[ticker].rename(columns=cash_flows[ticker].iloc[0,:], index=cash_flows[ticker].iloc[:,0])
    cash_flows[ticker] = cash_flows[ticker].drop(columns='Annual',index='Annual')
    balance_sheets[ticker] = balance_sheets[ticker].rename(columns=balance_sheets[ticker].iloc[0,:], index=balance_sheets[ticker].iloc[:,0])
    balance_sheets[ticker] = balance_sheets[ticker].drop(columns='Annual',index='Annual')


    if export_statements:
        
        with pd.ExcelWriter(str(export_statement_path) + str(ticker) + '.xlsx') as writer:
            income_statements[ticker].to_excel(writer, sheet_name='Income Statement')
            cash_flows[ticker].to_excel(writer, sheet_name='Cash Flow')
            balance_sheets[ticker].to_excel(writer, sheet_name='Balance Sheet')
        
        
        
###############################################################################
########################## Scrape and store betas #############################
###############################################################################
        
print("---- Scrape and store betas -----")

betas = {}
        
for ticker in tickers:

    url = "https://finance.yahoo.com/quote/" + ticker + "?p=" + ticker
    read_summary = ur.urlopen(url).read() 
    soup = BeautifulSoup(read_summary,"lxml")

    ls= [] 
    for l in soup.find_all("td"):          
        #Find all data structure that is ‘div’
        ls.append(l.string)
       
    betas[ticker] = pd.to_numeric(ls[19])
    print(ticker + " beta: " + str(betas[ticker]))   
    
    
###############################################################################
######################### Calculate Cost of Equity ############################
###############################################################################
        
print("---- Calculate Cost of Equity ----")

cost_of_equity = {}

for ticker in tickers:
    
    cost_of_equity[ticker] = risk_free_rate + (betas[ticker] * (expected_return - risk_free_rate))
    print(ticker + " Cost of Equity: " + str(cost_of_equity[ticker]))
    
    
# Note: CAPM Method
        
    
###############################################################################
########################## Calculate Cost of Debt #############################
############################################################################### 

print("---- Calculate Cost of Debt ----")    
    
cost_of_debt = {}

for ticker in tickers:
    
    if np.isnan(list(balance_sheets[ticker].loc['Long Term Debt'])[0]) != True:
        long_term_debt = list(balance_sheets[ticker].loc['Long Term Debt'])[0]
    else:
        long_term_debt = 0
        
    if np.isnan(list(income_statements[ticker].loc['Interest Expense'])[0]) != True:
        int_pmt = list(income_statements[ticker].loc['Interest Expense'])[0]
    else:
        int_pmt = 0
    
    if int_pmt == 0 or long_term_debt == 0:
        cost_of_debt[ticker] = 0
    else:
        cost_of_debt[ticker] = int_pmt / long_term_debt  
    print(ticker + " Cost of Debt: " + str(cost_of_debt[ticker]))
    

###############################################################################
#################### Calculate Debt and Equity Weights ########################
###############################################################################
    
print("---- Calculate Debt and Equity Weights ----")
    
equity_weight = {}
debt_weight = {}


for ticker in tickers:
    equity = list(balance_sheets[ticker].loc["Total stockholders' equity"])[0]
    if np.isnan(list(balance_sheets[ticker].loc['Long Term Debt'])[0]) != True:
        debt = list(balance_sheets[ticker].loc['Long Term Debt'])[0]
    else:
        debt = 0
    equity_weight[ticker] = equity / (equity + debt)
    debt_weight[ticker] = debt / (equity + debt)
    
    print(ticker + " Debt Weight: " + str(debt_weight[ticker]))
    print(ticker + " Equity Weight: " + str(equity_weight[ticker]))
    
    
###############################################################################
############################# Calculate WACC ##################################
###############################################################################
    
print("---- Calculate WACC ----")

wacc = {}

for ticker in tickers:
    
    wacc[ticker] = (cost_of_debt[ticker] * debt_weight[ticker] * (1 - tax_rate)) + (cost_of_equity[ticker] * equity_weight[ticker])
   
    print(ticker + " WACC: " + str(wacc[ticker]))
    
    
###############################################################################
############################# Calculate ROIC ##################################
###############################################################################    
 
print("---- Calculate ROIC ----")

roic = {}

for ticker in tickers:
    
    roic[ticker] = ( list(income_statements[ticker].loc["Operating Income or Loss"])[0] * ( 1 - tax_rate) ) / list(balance_sheets[ticker].loc["Total liabilities and stockholders' equity"])[0]
    print(ticker + " ROIC: " + str(roic[ticker]))
    

###############################################################################
############################# Calculate EVA ###################################
###############################################################################        

print("---- Calculate EVA ----")

eva = {}    
    
for ticker in tickers:

    eva[ticker] = roic[ticker] - wacc[ticker]
    print(ticker + " Economic Value Added: " + str(eva[ticker]))  
    
    

    
    
###############################################################################
################################### NOTES #####################################
###############################################################################     
##    
## 1.) WACC calculation ignores preferred stock  
##
## 2.) WACC uses a single tax rate for all firms
##    
## 3.) Using Long Term Debt and not total liabilties in wacc calc (maybe change that?)
##    
## 
##    
## 
##    
## 
##    
##     
##    
## 
##    
## 
##    
## 
##    
##  
## 
##    
## 
##    
## 
##    
##     