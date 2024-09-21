import sqlite3

conn = sqlite3.connect('C:/Users/minji/Desktop/Thesis/data_in/Scraped_Twitter/twitter_final.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS twitter
             (usertag text, date text, id text, tweet text, replies int, retweets int, likes int)''')
c.execute('''CREATE TABLE IF NOT EXISTS validator_replies
             (original text, usertag text, date text, id text, tweet text, replies int, retweets int, likes int)''')
c.execute('''CREATE TABLE IF NOT EXISTS influencer_replies
             (original text, usertag text, date text, id text, tweet text, replies int, retweets int, likes int)''')
c.execute('''CREATE TABLE IF NOT EXISTS likers
             (id text, likers text)''')
c.execute('''CREATE TABLE IF NOT EXISTS retweeters
             (id text, retweeters text)''')
