from twitterScraper import Scraper
import pandas as pd
import sqlite3
import datetime

if __name__ == "__main__":
    scraper = Scraper(manual_delay=30)
    start_date = datetime.date(2023, 5, 30) 
    end_date = datetime.date(2023, 5, 31)
    delta = datetime.timedelta(days=1)
    hashtags = '-grow17%2C%20-harvest17%2C%20-plant17%2C%20-corntownwtf%2C%20-vodka%2C%20-beer%2C%20-whisky%2C%20-whiskey%2C%20-recipe%2C%20-brew%2C%20-vegan%2C%20-keto%2C%20-gmo%2C%20-genome%2C%20-genotyp%2C%20-patholog%2C%20-pathogen%2C%20-agronomist%2C%20-phenotype%2C%20-phenolog%2C%20-agfact%2C%20-agtwitter%2C%20-funfact%2C%20-dyk%2C%20-pixel%2C%20-artist%2C%20-Etsy%2C%20-decor%2C%20-sustainab%2C%20-fanart%2C%20(%23wheat%20OR%20%23corn%20OR%20%23soybean%20OR%20%23oatt)%20min_faves%3A1'
 
    # $zc or $zs or $zw (exc. unrelated assets)
    # $weat or $corn or $soyb (exc. unrelated assets)
    
    while start_date <= end_date:
        next_day = start_date + delta
        print(scraper.scrape_request(hashtags, start_date.strftime('%Y-%m-%d'), next_day.strftime('%Y-%m-%d')))
        start_date += delta                                                                                                                     
        scraper.scraped_data
        # print('running 3')

    # update db
    conn = sqlite3.connect('C:/Users/minji/Desktop/Thesis/data_in/Scraped_Twitter/twitter_final.db')
    df = pd.DataFrame(scraper.scraped_data, columns=['usertag', 'date', 'id', 'tweet', 'replies', 'retweets', 'likes'])
    df.to_sql('twitter', conn, if_exists='append', index=False)
    print('{:>5,} tweets added.'.format(len(df)))

test = pd.read_sql_query("SELECT * FROM twitter", conn)
test
    