# All-You-Can-Scrape-Buffet
## TEMPLATE - reddit

1. add your reddit api to the top part of `scrape_reddit.py`

2. launch a jupyter notebook from the terminal

  `jupyter notebook`
  
3. run all cells in 'TEMPLATE-reddit.ipynb'


# Downloads Reddit Data 
## scrape subreddits, extract tickers, plot mentions, downloads and plots corresponding stock data

### scrape_reddit Function:
this function scrapes reddit subthread and extracts ticker symbols and then archives the thread titles as well as an index. 



### takes:
- category : 
    - parse data by:
    
        - 1.hot
        - 2.new
        - 3.con(controversial) 
        - 4.top 
        - 5.gilded
        
- stop_words : list words that might get confufuced with tickers if left blank it uses a list i have going in there. 
- subreddit : str sub-reddit you want to scrape ('wallstreetbets' by default)
- path : str


example:

    hot_df = scrape_reddit(category='hot',subreddit='wallstreetbets')
