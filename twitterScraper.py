from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from time import sleep
import re
from fake_useragent import UserAgent

ua = UserAgent()

class Scraper:
    def __init__(self, user_agent: str = ua.chrome, manual_delay: int = 60) -> None:
        self.user_agent = user_agent
        self.scraped_data = list()
        
        self._login(manual_delay)
        service = webdriver.ChromeService()
        self.driver = webdriver.Chrome(service=service)
                
    def _login(self, manual_delay: int) -> None:
        service = webdriver.ChromeService()
        temp_driver = webdriver.Chrome(service=service)
        temp_driver.get("https://twitter.com/login")
        time.sleep(manual_delay)
        temp_driver.quit()

    def scrape_request(self, q: str, since: str, until: str, exculde_replies: bool = True) -> list[dict]:
        assert until > since
    
        self.driver.get(f'https://twitter.com/search?q={q}%20lang%3Aen%20until%3A{until}%20since%3A{since}' #Language=en
                        + '%20-filter%3Areplies'*exculde_replies
                        + '&src=typed_query')
        
        scrollDelay = 0.1  # Delay between each scroll
        
        time.sleep(20)
        
        while 'Something went wrong' in self.driver.page_source:
            sleep(30)
            self.driver.refresh()
            sleep(5)
        
        try:
            articles = self.driver.find_elements(By.XPATH,"//article[@data-testid='tweet']") 
            #print(len(articles))
        except:
            raise Exception(RuntimeError)
        
        if len(articles) == 0:
            if 'No results for' in self.driver.page_source:   
                return []
            else: return None
            
        tweets = []
        # print('running 1')

        i = 100
        counter = 0
        while True:
            #print(len(articles))
            for article in articles:
                try:
                    tag = article.find_element(By.XPATH,".//*[@data-testid='User-Name']").text 
                    ts = article.find_element(By.XPATH,".//time").text #ok
                    id = article.find_element(By.XPATH,".//time/..").get_attribute('href') 
                    tweet = article.find_element(By.XPATH,".//*[@data-testid='tweetText']").text.strip().replace('\n', ' ') 
                    reply = article.find_element(By.XPATH,".//*[@data-testid='reply']").text
                    retweet = article.find_element(By.XPATH,".//*[@data-testid='retweet']").text
                    like = article.find_element(By.XPATH,".//*[@data-testid='like']").text
                    # print('ts:', ts)
                    # print('id:',id)
                    # print('tweet:',tweet)
                    # print('tag:',tag)
                    # print('reply:',reply)
                    # print('retweet:',retweet)
                    # print('like:',like)
                    
                    tweets.append({'usertag': tag, 
                    'date': ts,
                    'id':id,
                    'tweet': tweet,
                    'replies': reply,
                    'retweets': retweet, 
                    'likes': like,
                    })
                    # print('tweets list:', tweets)
                    # print('running 2')
                except:
                    pass
                    # print('passing')
            
            last_height = self.driver.execute_script("return window.pageYOffset")
            
            self.driver.execute_script(f"window.scrollBy(0, {i})")
            self.driver.implicitly_wait(scrollDelay)
            
            new_height = self.driver.execute_script("return window.pageYOffset")
            
            if last_height == new_height:
                counter += 1
                self.driver.implicitly_wait(scrollDelay*10)
            else:
                counter = 0
                
            if counter == 1:
                sleep(5)
            
            if counter == 5:
                break
            
            try:
                articles = self.driver.find_elements(By.XPATH,"//article[@data-testid='tweet']") 
            except:
                pass
        
        self.scraped_data += tweets
        self.scraped_data = [dict(t) for t in {tuple(d.items()) for d in self.scraped_data}]
        return tweets


    def scrape_replies(self, id: str) -> list[dict]:
        self.scraped_data = [] # reset for a new id
        self.driver.get(id)
        
        scrollDelay = 0.1  # Delay between each scroll
        
        time.sleep(20)
        
        while 'Something went wrong' in self.driver.page_source:
            sleep(30)
            self.driver.refresh()
            sleep(5)
        
        try:
            articles = self.driver.find_elements(By.XPATH,"//article[@data-testid='tweet']") 
        except:
            raise Exception(RuntimeError)
        
        if len(articles) == 0:
            if 'No results for' in self.driver.page_source:   
                return []
            else: return None
            
        tweets = []
                
        i = 100
        counter = 0
        while True:
            for article in articles:
                try:
                    tag = article.find_element(By.XPATH,".//div[@data-testid='User-Name']").text
                    ts = article.find_element(By.XPATH,".//time").text
                    id = article.find_element(By.XPATH,".//time/..").get_attribute('href')
                    tweet = article.find_element(By.XPATH,".//div[@data-testid='tweetText']").text.strip().replace('\n', ' ')
                    reply = article.find_element(By.XPATH,".//div[@data-testid='reply']").text
                    retweet = article.find_element(By.XPATH,".//div[@data-testid='retweet']").text
                    like = article.find_element(By.XPATH,".//div[@data-testid='like']").text
                    
                    tweets.append({'usertag': tag, 
                    'date': ts,
                    'id':id,
                    'tweet': tweet,
                    'replies': reply,
                    'retweets': retweet, 
                    'likes': like,
                    })
                except:
                    pass
                    
            
            last_height = self.driver.execute_script("return window.pageYOffset")
            
            self.driver.execute_script(f"window.scrollBy(0, {i})")
            self.driver.implicitly_wait(scrollDelay)
            
            new_height = self.driver.execute_script("return window.pageYOffset")
            
            if last_height == new_height:
                counter += 1
                self.driver.implicitly_wait(scrollDelay*10)
            else:
                counter = 0
                
            if counter == 1:
                sleep(5)
            
            if counter == 5:
                break
            
            try:
                articles = self.driver.find_elements(By.XPATH,"//article[@data-testid='tweet']") 
            except:
                pass
        
        self.scraped_data += tweets
        self.scraped_data = [dict(t) for t in {tuple(d.items()) for d in self.scraped_data}]
        return tweets


    def scrape_retweeters(self, id: str) -> list[dict]:
        
        self.scraped_data = [] # reset for a new id
        self.driver.get(f'{id}/retweets')
        
        scrollDelay = 0.01  # Delay between each scroll
        
        time.sleep(10)
        
        while 'Something went wrong' in self.driver.page_source:
            sleep(30)
            self.driver.refresh()
            sleep(5)
        
        try:
            users = self.driver.find_elements(By.XPATH,"//div[@data-testid='cellInnerDiv']") 
        except:
            raise Exception(RuntimeError)
        
        if len(users) == 0:
            if 'No results for' in self.driver.page_source:   
                return []
            else: return None
            
        retweet_by = []
        pattern = r'\n(.*?)\n'
                
        i = 30
        counter = 0
        while True:
            for user in users:
                try:
                    name = user.find_element(By.XPATH,".//*[@data-testid='UserCell']").text
                    match = re.search(pattern, name)
                    tag = match.group(1)
                    retweet_by.append(tag)
                except:
                    pass 
            
            last_height = self.driver.execute_script("return window.pageYOffset")
            
            self.driver.execute_script(f"window.scrollBy(0, {i})")
            self.driver.implicitly_wait(scrollDelay)
            
            new_height = self.driver.execute_script("return window.pageYOffset")
            
            if last_height == new_height:
                counter += 1
                self.driver.implicitly_wait(scrollDelay*10)
            else:
                counter = 0
                
            if counter == 1:
                sleep(5)
            
            if counter == 5:
                break
            
            try:
                users = self.driver.find_elements(By.XPATH,"//div[@data-testid='cellInnerDiv']")  
            except:
                pass
        
        self.scraped_data += retweet_by

        return retweet_by


    def scrape_likers(self, id: str) -> list[dict]:
        
        self.scraped_data = [] # reset for a new id
        self.driver.get(f'{id}/likes')
        
        scrollDelay = 0.01  # Delay between each scroll
        
        time.sleep(10)
        
        while 'Something went wrong' in self.driver.page_source:
            sleep(30)
            self.driver.refresh()
            sleep(5)
        
        try:
            users = self.driver.find_elements(By.XPATH,"//div[@data-testid='cellInnerDiv']")
        except:
            raise Exception(RuntimeError)
        
        if len(users) == 0:
            if 'No results for' in self.driver.page_source:   
                return []
            else: return None
            
        like_by = []
        pattern = r'\n(.*?)\n'
                      
        i = 30
        counter = 0
        while True:
            for user in users:
                try:
                    name = user.find_element(By.XPATH,".//*[@data-testid='UserCell']").text
                    match = re.search(pattern, name)
                    tag = match.group(1)
                    like_by.append(tag)
                except:
                    pass 
            
            last_height = self.driver.execute_script("return window.pageYOffset")
            
            self.driver.execute_script(f"window.scrollBy(0, {i})")
            self.driver.implicitly_wait(scrollDelay)
            
            new_height = self.driver.execute_script("return window.pageYOffset")
            
            if last_height == new_height:
                counter += 1
                self.driver.implicitly_wait(scrollDelay*10)
            else:
                counter = 0
                
            if counter == 1:
                sleep(5)
            
            if counter == 5:
                break
                
            try:
                users = self.driver.find_elements(By.XPATH,"//div[@data-testid='cellInnerDiv']")  
            except:
                pass
        
        
        self.scraped_data += like_by

        return like_by

    def clean_buffer(self) -> None:
        self.scraped_data.clear()


