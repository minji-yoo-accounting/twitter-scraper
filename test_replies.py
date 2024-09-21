from twitterScraper import Scraper
import pandas as pd
import sqlite3


df = pd.read_csv('C:/Users/minji/Desktop/Thesis/data_in/Scraped_Twitter/twitter_original_with_replies.csv')
id_list = df['id'].to_list()


if __name__ == "__main__":
    
    conn = sqlite3.connect('C:/Users/minji/Desktop/Thesis/data_in/Scraped_Twitter/twitter_new.db')
    scraper = Scraper(manual_delay=30)
    print(scraper.scrape_request('(%23grainfutures)', '2022-01-01', '2022-01-02')) # dummy search to trigger login
    for id in id_list: 
        print(scraper.scrape_replies(id))
        # print(scraper.scrape_retweeters(id))
        # print(scraper.scrape_likers(id)) 
        print(scraper.scraped_data)  

        df = pd.DataFrame(scraper.scraped_data, columns=['usertag', 'date', 'id', 'tweet', 'replies', 'retweets', 'likes'])
        print(df)
        # df.to_sql('twitter', conn, if_exists='append', index=False)
        # print('{:>5,} tweets added.'.format(len(df)))

# test = pd.read_sql_query("SELECT * FROM replies LIMIT(100)", conn)
# test
    
