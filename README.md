This repository contains the Twitter scraper I used for my dissertation, **"Information Sharing for Validation: Evidence from Social Networks."**

The scraper includes four main functions:

- scrape_request: Extracts the user tag, ID, main post, and the number of replies, retweets, and likes based on a search query.
- scrape_replies: Extracts the user tag, ID, main post, and the number of replies, retweets, and likes of the replies, using the ID of the original post.
- scrape_retweeters: Extracts a list of retweeters of a post, using the ID of the original post.
- scrape_likers: Extracts a list of likers of a post, using the ID of the original post.

**Legal Disclaimer**: The author complied with X.com (Twitter)'s code of conduct during the web scraping process. Posts are collected using the log-in information of the author's verified X.com account, respecting the daily user view limit (10,000 posts per day for a premium user.) The paper does not make use of any personally identifiable information or copyright-protected content.


**Note**: The scraper worked as of May 2024. Due to frequent changes in the HTML structure of X.com and updates to the Python packages used in the scraper, some adjustments may be needed to ensure it functions properly. For reference, I had to make 2-3 major adjustments to the scraper over a five-month period (January 2023 - May 2023). Additionally, please note that there are various approaches to scraping X.com.
