# SinaWeiboCrawler
<b>Introduction<b/><br><br/>
This is a simple function to crawl Sina Weibo from your homepage and conduct sentiment analysis by using Naive Bayes. Considering that author usually login from the United States, the page after logging in might be slightly different in China or other countries. Please find the main page (or "首页") and kick off the script.

<b>Functions Introduction<b/>

1. find_username - to find the main username and forward username of that one weibo
2. find_content - to find main content and forward content of that one weibo
3. find_time - to find published time for main content and forward content of that one weibo
4. find_page_bottom - scroll down the bottom of page
5. load_allpage - work with function, 'find_page_bottom' to make sure we collect all weibos on that page
6. login - function to log in weibo
7. check_date - find those weibo published after the specific date
8. collect_weibo - main function to collect weibo
9. weibo_crawl - recursive function to crawl weibo from different users' pages

<b>Final Output<b/><br><br/>
The results would be saved in weibo_rows like following: [["weibo_users","main_content","main_published_time","forward_weibo_users","forward_content","forward_published_time"]]

Please feel free to contact with me through email if you find any bugs or difficuties to use the script. My email is <b>jasonwangumd@gmail.com<b/>
