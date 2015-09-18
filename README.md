# SinaWeiboCrawler
<b>Introduction</b><br></br>
This is a simple function to crawl Sina Weibo from your homepage and conduct sentiment analysis by using Naive Bayes. Considering that author usually login from the United States, the page after logging in might be slightly different in China or other countries. Please find the main page (or "首页") and kick off the script.

<b>Functions Introduction</b>

1. find_username - to find the main username and forward username of that one weibo
2. find_content - to find main content and forward content of that one weibo
3. find_time - to find published time for main content and forward content of that one weibo
4. find_page_bottom - scroll down the bottom of page
5. load_allpage - work with function, 'find_page_bottom' to make sure we collect all weibos on that page
6. login - function to log in weibo
7. check_date - find those weibo published after the specific date
8. collect_weibo - main function to collect weibo
9. weibo_crawl - recursive function to crawl weibo from different users' pages

<b>Final Output</b><br></br>
The results would be saved in weibo_rows like following: [["weibo_users","main_content","main_published_time","forward_weibo_users","forward_content","forward_published_time"]]

Please feel free to contact with me through email if you find any bugs or difficuties to use the script. My email is <b>jasonwangumd@gmail.com</b>


#Naive Bayes Sentiment Analysis

After collecting weibo, I used Naive Bayes algorithm to analyze sentiment of each weibo. First, I mannually marked whether that weibo is positive or negative. The main purpose of the sentiment analysis is to use in stock market or financial industry. 

Final output from the sentiment analysis looks like following:

全球危机继中国A股再次大跌之后月日亚洲欧洲美国股市先后传来大跌声纷纷创下阶段性低点商品市场也哀鸿一片国际油价盘中跌破美元桶铜价继续下挫逼近六年新低
negative

全球股市大跌目前美洲非洲地区还未开盘
negative

利好大金融华泰证券罗毅表示总量万亿的养老金按照的比例投资股市有望带动万亿资金入市长线资金的入市从历史时期可以看都表明此位置是市场的阶段性底部巨量资金的入市将利好大金融等蓝筹股网页链接
positive

