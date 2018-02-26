# -*- coding: utf-8 -*-
"""
Sarah Wigodsky
DATA 602 Advanced Programming
Assignment 1
"""
import bs4          #import BeautifulSoup4 for process information from webpages
import urllib.request      #to process urls
import time
import datetime            #to determine the current date and time 

def main_menu():    #function prints the menu on the screen and returns inputted value   print('Choose one of the following numbered options\n')
    number = '0'
    x = ['1','2','3','4']
    while number not in x:
        print('1. Trade\n')
        print('2. Blotter\n')
        print('3. Show P/L\n')
        print('4. Quit\n')
        number = input('Input the Number ')
    return(int(number))

def buy_sell_menu():   #function to ask user if he/she wants to buy or sell
    number = '0'
    x = ['1','2']
    while number not in x:
        print('Would you like to buy or sell?\n')
        print('1. Buy\n')
        print('2. Sell\n')
        number = input('Input the Number ')
    return(number)

def number_shares(side):  #user chooses number of shares to buy or sell
    while True:     
        try:
            num_shares = int(input('How many shares would you like to '+ side + ' ?'))
        except ValueError:
            print('Choose a number')
            continue
        else:
            break
    return(num_shares)    
    
def check_num_shares_owned(equity_num, blotter):  #check if any shares of equity to be bought or sold are already owned by user
    options = {1: 'AMZN', 2: 'BKS', 3: 'COF', 4: 'PG', 5: 'SNE'}
    ticker = options.get(equity_num,0)
    num_shares = 0
    
    for item in blotter:
        if item[1]==ticker:
            if item[0]=='buy':
                num_shares = num_shares+item[2]
            else:
                num_shares = num_shares-item[2]
    return(num_shares)
    

def yahoo_scraping(equity_num, side): #scraping Yahoo for asking or selling price
    #if side=='buy':
    options = {1: "https://finance.yahoo.com/quote/AMZN?p=AMZN", 2: "https://finance.yahoo.com/quote/bks?p=bks", 3: "https://finance.yahoo.com/quote/COF?p=COF", 4: "https://finance.yahoo.com/quote/PG?p=PG", 5: "https://finance.yahoo.com/quote/sne?p=sne"}  
    url = options.get(equity_num,0)
    page = urllib.request.urlopen(url)
    soup = bs4.BeautifulSoup(page.read(),"lxml")
    if side=='buy':
        bid_ask = soup.find('td', attrs={'data-test': 'ASK-value'}).get_text()
    else:
        bid_ask = soup.find('td', attrs={'data-test': 'BID-value'}).get_text()
      
    for index in range(len(bid_ask)):
        if bid_ask[index]==" ":
            break
    counter=index
    bid_ask = bid_ask[0:counter+1]
    bid_ask = bid_ask.replace(',','')
    return(float(bid_ask))

def confirmation():  #function to confirm if user wants to buy stock
    choice = ["Y","N"]
    confirm="A"
    while (confirm not in choice):
        confirm = input("Are you still interested in buying this stock? Input Y/N\n")
        confirm = confirm.upper()
    if confirm =="Y":
        print('You chose to buy the equity.\n')
        return(1)
    else:
        print('You chose not to go ahead with the buy.\n')
        return(0)

def transaction_cost(blotter,side,bid_ask,num_shares, ticker, st):    #calculating cost of sale and amount of money left in cash
    cost = num_shares*bid_ask
    if len(blotter)==1:
        cash = 10000000
    else:
        cash = blotter[-1][6]
    if side == 'buy':
        if cash >= cost:
            cash = round(cash - cost,2)    
            blotter_add = [side,ticker,num_shares,bid_ask,st,cost,cash]
            blotter.append(blotter_add)
            print('The cost of the transaction is ' + str(cost))
            print('You currently have $' + str(cash) + ' available in cash')
            return(blotter)
        else:
            print("You don't have enough money for this transaction.")
            print('You currently have $' + str(cash) + ' available in cash')
            print("The transaction would have cost $" +str(cost))
            return(0)
    else:
        cash = round(cash + cost,2)            
        blotter_add = [side,ticker,num_shares,bid_ask,st,cost,cash]
        blotter.append(blotter_add)
        print('On this transaction, you are making ' + str(cost) + '\n')
        print('You currently have $' + str(cash) + ' available in cash')
        return(blotter)
    
def trade(cash, blotter): #trading function
    number = '0'
    x = ['1','2','3','4', '5']
    while number not in x:      #user chooses an equity from the list
        print('Choose one of the following equities to buy or sell\n')
        print('1. Amazon AMZN\n')
        print('2. Barnes & Noble BKS\n')
        print('3. Capital One COF\n')
        print('4. Procter & Gamble PG\n')
        print('5. Sony SNE\n')
        number = input('Input the Number \n')
    print('you chose ' + number)
    
    if number == '1':  #user chose Amazon
        ticker = 'AMZN'
        buy_sell = buy_sell_menu()
        if buy_sell =='1':  #if buying 
            side = 'buy'
            num_shares = number_shares(side) #calling function to find num of shares user wants to buy
            ask = yahoo_scraping(1,'buy')   #calling function to scrape Yahoo for asking price          
            ts = time.time()  #time stamp for buy
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')  
            print("The asking price for Amazon is " + str(ask))
            check = confirmation()
            if check == 0:
                return(blotter)
            value = transaction_cost(blotter, side, ask, num_shares, ticker, st)
            if value ==0:
                return(blotter)
            else: 
                return(value)

        else:   #if selling Amazon
            side = 'sell'
            num_shares = check_num_shares_owned(1, blotter)
            num_shares_sell = 100000000000
            print('You have ' +str(num_shares) + ' of Amazon\n.')
            if num_shares==0:
                print('You have no shares of Amazon to sell.')
                return(blotter)
            else:
                while (num_shares_sell > num_shares):
                    num_shares_sell = number_shares(side)
            bid = yahoo_scraping(1,'sell')
            ts = time.time()  #time stamp for buy
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            print("The selling price for Amazon is " + str(bid))
            blotter = transaction_cost(blotter, side, bid, num_shares_sell, ticker, st) 
            return(blotter)
            
    if number == '2':  #user chose Barnes and Noble
        ticker = 'BKS'
        buy_sell = buy_sell_menu()
        if buy_sell =='1':  #if buying 
            side = 'buy'
            num_shares = number_shares(side) #calling function to find num of shares user wants to buy
            ask = yahoo_scraping(2,'buy')   #calling function to scrape Yahoo for asking price          
            ts = time.time()  #time stamp for buy
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')  
            print("The asking price for Barnes and Noble is " + str(ask))
            check = confirmation()
            if check == 0:
                return(blotter)
            value = transaction_cost(blotter, side, ask, num_shares, ticker, st)
            if value ==0:
                return(blotter)
            else: 
                return(value)

        else:   #if selling 
            side = 'sell'
            num_shares = check_num_shares_owned(2, blotter)
            num_shares_sell = 100000000000
            print('You have ' +str(num_shares) + ' of Barnes and Noble\n.')
            if num_shares==0:
                print('You have no shares of Barnes and Noble to sell.')
                return(blotter)
            else:
                while num_shares_sell > num_shares:  #checking that user is selling shares that are less than or equal to current position
                    num_shares_sell = number_shares(side)
            bid = yahoo_scraping(2,'sell')
            ts = time.time()  #time stamp
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            print("The selling price for Barnes & Noble is " + str(bid))
            blotter = transaction_cost(blotter, side, bid, num_shares_sell, ticker, st) 
            return(blotter)
    
    if number == '3':  #user chose Capital One
        ticker = 'COF'
        buy_sell = buy_sell_menu()
        if buy_sell =='1':  #if buying 
            side = 'buy'
            num_shares = number_shares(side) #calling function to find num of shares user wants to buy
            ask = yahoo_scraping(3,'buy')   #calling function to scrape Yahoo for asking price          
            ts = time.time()  #time stamp for buy
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')  
            print("The asking price for Capital One is " + str(ask))
            check = confirmation()
            if check == 0:
                return(blotter)
            value = transaction_cost(blotter, side, ask, num_shares, ticker, st)
            if value ==0:
                return(blotter)
            else: 
                return(value)

        else:   #if selling 
            side = 'sell'
            num_shares = check_num_shares_owned(3, blotter)
            num_shares_sell = 100000000000
            print('You have ' +str(num_shares) + ' of Capital One\n.')
            if num_shares==0:
                print('You have no shares of Capital One to sell.')
                return(blotter)
            else:
                while num_shares_sell> num_shares:
                    num_shares_sell = number_shares(side)
            bid = yahoo_scraping(3,'sell')
            ts = time.time()  #time stamp for sell
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            print("The selling price for Capital One is " + str(bid))
            blotter = transaction_cost(blotter, side, bid, num_shares_sell, ticker, st) 
            return(blotter)    
    
    if number == '4':  #user chose Proctor & Gamble
        ticker = 'PG'
        buy_sell = buy_sell_menu()
        if buy_sell =='1':  #if buying 
            side = 'buy'
            num_shares = number_shares(side) #calling function to find num of shares user wants to buy
            ask = yahoo_scraping(4,'buy')   #calling function to scrape Yahoo for asking price          
            ts = time.time()  #time stamp for buy
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')  
            print("The asking price for Proctor & Gamble is " + str(ask))
            check = confirmation()
            if check == 0:
                return(blotter)
            value = transaction_cost(blotter, side, ask, num_shares, ticker, st)
            if value ==0:
                return(blotter)
            else: 
                return(value)

        else:   #if selling 
            side = 'sell'
            num_shares = check_num_shares_owned(4, blotter)
            num_shares_sell = 100000000000
            print('You have ' +str(num_shares) + ' of Proctor & Gamble\n.')
            if num_shares==0:
                print('You have no shares of Proctor & Gamble to sell.')
                return(blotter)
            else:
                while num_shares_sell> num_shares:
                    num_shares_sell = number_shares(side)
            bid = yahoo_scraping(4,'sell')
            ts = time.time()  #time stamp for sell
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            print("The selling price for Proctor & Gamble is " + str(bid))
            blotter = transaction_cost(blotter, side, bid, num_shares_sell, ticker, st) 
            return(blotter)    

    if number == '5':  #user chose Sony
        ticker = 'SNE'
        buy_sell = buy_sell_menu()
        if buy_sell =='1':  #if buying 
            side = 'buy'
            num_shares = number_shares(side) #calling function to find num of shares user wants to buy
            ask = yahoo_scraping(5,'buy')   #calling function to scrape Yahoo for asking price          
            ts = time.time()  #time stamp for buy
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')  
            print("The asking price for Sony is " + str(ask))
            check = confirmation()
            if check == 0:
                return(blotter)
            value = transaction_cost(blotter, side, ask, num_shares, ticker, st)
            if value ==0:
                return(blotter)
            else: 
                return(value)

        else:   #if selling
            side = 'sell'
            num_shares = check_num_shares_owned(5, blotter)
            num_shares_sell = 100000000000
            print('You have ' +str(num_shares) + ' of Sony\n.')
            if num_shares==0:
                print('You have no shares of Sony to sell.')
                return(blotter)
            else:
                while num_shares_sell> num_shares:
                    num_shares_sell = number_shares(side)
            bid = yahoo_scraping(5,'sell')
            ts = time.time()  #time stamp for sell
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            print("The selling price for Sony is " + str(bid))
            blotter = transaction_cost(blotter, side, bid, num_shares_sell, ticker, st) 
            return(blotter)
    
def print_blotter(blotter):
    for item in blotter:
        print("|",item[0]," "*(4-len(item[0])),"|",item[1]," "*(6-len(item[1])),"|",item[2]," "*(8-len(str(item[2]))),"|",item[3]," "*(14-len(str(item[3]))),"|",item[4]," "*(15-len(str(item[4]))),"|",item[5]," "*(12-len(str(item[5]))),"|")
    print('\n')    
    
def updating_pl_values(blotter,pltable,equity_index,ticker):
    bid = yahoo_scraping(ticker,'sell')
    pltable[ticker][2] = bid  #setting the current market price to sell 
    for i,j in equity_index:
        if blotter[i][0]=='buy':
            wap = (pltable[ticker][3]*pltable[ticker][1] + blotter[i][3]*blotter[i][2])/(pltable[ticker][1]+blotter[i][2]) #calculating weighted average price per share 
            pltable[ticker][3] = round(wap,2)
            position = pltable[ticker][1] + blotter[i][2]  #adding number of shares bought to position
            pltable[ticker][1] = position
            upl = (bid-wap)*position
            pltable[ticker][4] = round(upl,2)
        else:
            position = pltable[ticker][1] - blotter[i][2]  #subtracting number of shares bought from position
            pltable[ticker][1] = position
            rpl = pltable[ticker][5]+ blotter[i][2]*blotter[i][3]  #calculating realized profit
            pltable[ticker][5] = round(rpl,2)
            upl = position*(bid-pltable[ticker][3])  #calculating new unrealized profit/loss
            pltable[ticker][4] = round(upl,2)
    return(pltable)

def profit_loss(blotter):
    pltable = [['Ticker','Position','Market','WAP','UPL','RPL'],['AMZN',0,'',0,0,0],['BKS',0,'',0,0,0],['COF',0,'',0,0,0],['PG',0,'',0,0,0],['SNE',0,'',0,0,0],['Cash',0,0,' ',' ',' ']]
    if len(blotter)==1:
        pltable[6][1] = 10000000 #cash on hand
        pltable[6][2] = 10000000 
    
    else:
        amzn_index=[(i, value.index('AMZN')) for i, value in enumerate(blotter) if 'AMZN' in value]
        bks_index=[(i, value.index('BKS')) for i, value in enumerate(blotter) if 'BKS' in value]
        cof_index=[(i, value.index('COF')) for i, value in enumerate(blotter) if 'COF' in value]
        pg_index=[(i, value.index('PG')) for i, value in enumerate(blotter) if 'PG' in value]
        sne_index=[(i, value.index('SNE')) for i, value in enumerate(blotter) if 'SNE' in value]
        
        if amzn_index != []:
            pltable = updating_pl_values(blotter, pltable, amzn_index,1)
        if bks_index != []:
            pltable = updating_pl_values(blotter, pltable, bks_index,2)
        if cof_index != []:
            pltable = updating_pl_values(blotter, pltable, cof_index,3)
        if pg_index != []:
            pltable = updating_pl_values(blotter, pltable, pg_index,4)
        if sne_index != []:
            pltable = updating_pl_values(blotter, pltable, sne_index,5)

        pltable[6][1] = blotter[-1][6] #cash on hand
        pltable[6][2] = blotter[-1][6] 
            
    for item in pltable:
        if item[0] != 'Ticker' and item[0] != 'Cash':
            item[5] = round(item[5],2)
        print("|",item[0]," "*(10-len(item[0])),"|",item[1]," "*(10-len(str(item[1]))),"|",item[2]," "*(10-len(str(item[2]))),"|",item[3]," "*(10-len(str(item[3]))),"|",item[4]," "*(10-len(str(item[4]))),"|",item[5]," "*(10-len(str(item[5]))),"|")
    print('\n')        

    
cash = 10000000
blotter=[['Side','Ticker','Quantity','Executed Price','Execution Timestamp', 'Money In/Out', 'Cash on Hand']]

choice = 5
while choice != 4:
    choice = main_menu()
    print ('You chose ' + str(choice))

    if choice == 1:
        blotter = trade(cash, blotter)

    elif choice == 2:
        print_blotter(blotter)
        
    elif choice == 3:
        profit_loss(blotter)

