import string
import re
import cufflinks as cf
cf.go_offline(connected=False)
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import praw
import pandas as pd
import os
from datetime import datetime


boring = ['url','Datetime']

secret     = ''
user_secret= ''
ID         = ''
user_agent = ''  
user_name  = ''
password   = ''


reddit = praw.Reddit(client_id=ID, 
                    client_secret=user_secret,
                    user_agent=user_agent,
                    username=user_name,
                    password=password)



#!/usr/bin/env python
import re

text = u'This is a smiley face \U0001f602'
print(text) # with emoji

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

print(deEmojify(text))

def extract_tickers(text):
#print(text)
    # this makes sure the whole daymn title isnt in CAPS
    if text != text.upper():
        #removing numbers
        text = re.sub(r'\d+', '', text)
        # remove emojis
        text = deEmojify(text)
        #splitting word up
        text = word_tokenize(text)
        
        text = [l for l in text if l not in string.punctuation]
        text = [word for word in text if not word in stopwords.words('english')]
        text = ' '.join(text)
        # only collect small words
        smal = [word for word in text.split() if (2<len(word)<5)]


        cap_n_smal = []
        for word in smal:
            if word.lower() != word.upper():
                new_word = [l for l in word.split() if l == l.upper()]
                new_word = ''.join(new_word)
                #print(new_word)
                if (len(new_word) == len(word)):
                    cap_n_smal.append(word)

        tics = [w for w in cap_n_smal if w not in stop_words]
        #print(text,'\n')
        #print(smal,'\n')
        #print(cap_n_smal,'\n')
        #print(tics)
    else:
        tics = []
    return tics

def save_function(hdf,category,path='reddit_archive/'):
    '''
    saves the parsed Post topics for the archive...
    '''
    
    sheet_name = path+category + '.csv'
    hdf['Datetime'] = datetime.now() 
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(sheet_name):
        hdf.to_csv(sheet_name,index=False)
    else:
        odf = pd.read_csv(sheet_name)
        ndf = odf.append(hdf)
        ndf.to_csv(sheet_name,index=False)

def tics_to_cols(hdf):

    for i in range(len(hdf)):
        for tic in hdf['tics'][i]:
            if tic not in hdf.columns:
                hdf[tic] = 0
                hdf[tic][i] = 1
            else:
                hdf[tic][i] = 1

    # make a new df for tickers
    not_tickers = ['url','tics']
    tdf         = hdf.drop(not_tickers,axis=1)
    
    #tdf.sum().iplot(theme='solar',kind='bar',title=category)
    
    
    #BOOM! 

    return hdf

stop_words = ['HOLD','WSB','PSA','NYT','WSJ','FUCK','CNBC','AOC','SEC','CNN','FOR','THE','BROS','KEEP','GOT','DFV',
             'NOT','SELL','THEM','AND','HAVE','MORE','THAN','WILL','...']
go_words   = ['HOLD','to the moon','$','DFV']



def scrape_reddit(category,stop_words=None,subreddit='wallstreetbets',path='reddit_archive/'):
    '''
    this thing srapes reddit for you and grabs the categyory you specigy
    categorys:
        1. hot
        2. new
        3. con    = controversial
        4. top
        5. gilded = gifted gold
    '''
    if stop_words == None:
        stop_words = ['HOLD','WSB','PSA','NYT','WSJ','FUCK','CNBC','AOC','SEC','CNN','FOR','THE','BROS','KEEP','GOT','DFV',
             'NOT','SELL','THEM','AND','HAVE','MORE','THAN','WILL','...','DID',"N'T",'HEAR','OUT','BEG','NOW','GOES','SOLD','WENT','MOON','BUST','PLAY','ITM','NYC','LIKE','FLEX','WEED','GOOD','JOB','HEAR','OUT','INTO','END']
    #create subreddit instance
    subred = reddit.subreddit(subreddit)
    
    # select thread to parse
    if category == 'hot' :
        reddit_instance = subred.hot(limit=100)
    if category == 'new' :
        reddit_instance = subred.new(limit=100)
    if category == 'con' :
        reddit_instance = subred.controversial(limit=100)
    if category == 'top' :
        reddit_instance = subred.top(limit=100)
    if category == 'gilded' :
        reddit_instance = subred.gilded(limit=100)

    # here we just want to title and url for reference                  
    hot_li = []
    for i in reddit_instance:
        #print(i.title,i.url)
        hot_dic = {}
        hot_dic['title'] = i.title
        hot_dic['url']   = i.url
        hot_li.append(hot_dic)

    # DataFrame
    hdf = pd.DataFrame(hot_li)
    
    # SAVING TITLES 
    save_cat    = subreddit + '_' + category
    hdf['tics'] = hdf['title'].apply(extract_tickers)
    hdf         = tics_to_cols(hdf)
    save_function(hdf,save_cat)
    
    # ONLY SHOW TICKERS THAT HAVE BEEN MENTIONED MORE THAN ONCE
    not_tickers = ['Datetime','url','tics','title']
    great = pd.DataFrame(hdf.drop(not_tickers,axis=1).sum()>2)
    great = great[great[0]==True].index    
    
    gdf   = hdf[great]
    # plot
    gdf.sum().iplot(theme='solar',kind='bar',title=save_cat)

    gdf['scrape_date'] = datetime.now()
    gdf                = gdf.set_index('scrape_date')
    gdf

    # SAVING A TICKER INDEX
    ticker_index_sheet = path + 'TickerIndex_'+save_cat + '.csv'
    # cheack if the path exists 
    if not os.path.exists(ticker_index_sheet):
        gdf.to_csv(ticker_index_sheet)
        print('ticker index dont exist')
    else:
        odf = pd.read_csv(ticker_index_sheet)
        ndf = odf.append(gdf)
        ndf.to_csv(ticker_index_sheet)
        print('TICKER INDEX UPDATED!')
        col_delta = len(ndf.columns) - len(odf.columns)
        print('There Are {} new Tickers'.format(col_delta))
        if col_delta > 0:
            new_cols = list(ndf.drop(odf.columns,axis=1).columns)
            [print(new) for new in new_cols]
        
    return hdf


def hl(df):
    def highlight(boo):
        criteria = boo == True
        return ['background-color: green' if i else '' for i in criteria]
    df = df.style.apply(highlight)
    return df