# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import time
from random import choice
import re
from bs4 import BeautifulSoup
from datetime import datetime,date


def find_username(feed_block):
    #find weibo original username  
    original_name = feed_block.find("a",{"class":"W_f14 W_fb S_txt1"})
    if original_name != None:
        original_name = original_name.text.strip()
    
    
    #find weibo forward username
    forward_name = feed_block.find("a",{"class":"W_fb S_txt1"})
    if forward_name != None:
        forward_name = forward_name.text.strip()
    
    return [original_name, forward_name]


def find_content(feed_block):
    #find weibo original content
    original_text = feed_block.find("div",{"class":"WB_text W_f14","node-type":"feed_list_content"})
    if original_text != None:
        original_text = original_text.text
    
    #find weibo forward content
    foward_text = feed_block.find("div",{"class":"WB_text","node-type":"feed_list_reason"})
    if foward_text != None:
        foward_text = foward_text.text
    
    return [original_text, foward_text]


def find_time(feed_block):
    
    times = feed_block.find_all("a",{"class":"S_txt2","node-type":"feed_list_item_date"})
    
    original_time = None
    forward_time = None
    
    if times!=None:
        if len(times) == 2:
            #find weibo forward content
            original_time = times[1]['title']
            #find weibo forward content
            forward_time = times[0]['title']
        elif len(times) == 1:
            original_time = times[0]['title']
     
    return [original_time, forward_time]


##to find the bottome (下一页） 
def find_page_bottom(driver):
    tem_soup = BeautifulSoup(driver.page_source)
    find = tem_soup.find("a",{'class':'page next S_txt1 S_line1'})
    if find != None:
        find_url = find['href']
        current_url = driver.current_url
        next_link = re.findall(u'http://.*?/', current_url)[0] + find_url[1:]
    else:
        next_link = None
    return next_link


def load_allpage(driver,limit):
    for try_time in range(3): #usally we only need to scroll 3 times to get bottom page
        sleep(3)
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    nextpage_check = find_page_bottom(driver)
    if nextpage_check != None:
        return nextpage_check
    elif limit != 0: ##To avoid infinite loop and those hidden weibos
        browser.refresh() #avoid stuck on “正在加载更多"
        return load_allpage(driver,limit-1)
    else:
        return None


def check_date(date_string,expect_date):
    if date_string is None:
        return True
    else:
        weibo_date = datetime.strptime(date_string, '%Y-%m-%d %H:%M')
        if weibo_date >= expect_date:
            return True
        else:
            return False


def login(username,password):
    wait.until(lambda browser: browser.find_element_by_xpath('//input[@name="username"][@node-type="username"]')) #等待登录页面出现
    user = browser.find_element_by_xpath('//input[@name="username"][@node-type="username"]')
    user.clear()
    user.send_keys(username) #输入用户名
    psw = browser.find_element_by_xpath('//input[@name="password"][@node-type="password"]')
    psw.clear()
    psw.send_keys(password) #输入密码
    browser.find_element_by_xpath('//a[@action-type="btn_submit"][@node-type="submitBtn"]').click() #点击“登录”


def collect_weibo(expect_date, url, is_home_page,username=None): #is_home_page 1 home_page 0 other weibo homepage
    global weibo_rows
    
    refresh_limit = 10
    href_user_dict = {}
    
    if len(re.findall('http://sass.weibo.com.*',browser.current_url)) != 0: ##to avoid CAPTCHA
        print(browser.current_url)
        sleep(300)
        
    browser.get(url)
    
    if is_home_page == 0:
        try:
            wait.until(lambda browser: browser.find_element_by_tag_name('strong'))
        except TimeoutException:
            try: 
                browser.find_element_by_xpath('//span[@class="S_txt1 t_link"]').click()
            except NoSuchElementException:
                print(browser.current_url, "doesn't get valid weibo page format")
                return None
            
        num_weibo = int(browser.find_elements_by_tag_name('strong')[2].text)
        nextpage_button = load_allpage(browser,refresh_limit)
        n_page = 2
        
        if num_weibo <= 45:
            n_page = 1 #change home page number
    else:
        nextpage_button = load_allpage(browser,refresh_limit)
        n_page = 10
    
    for page_num in range(n_page):
        if page_num < n_page-1 and page_num >0:
            nextpage_button = load_allpage(browser,refresh_limit)
        weibo_soup = BeautifulSoup(browser.page_source)
        for each_feed in weibo_soup.find_all("div",{"class":"WB_feed_detail clearfix","node-type":"feed_content"}):
            users = find_username(each_feed)
            text = find_content(each_feed)
            weibo_time = find_time(each_feed)
            
            if check_date(weibo_time[0],expect_date):
                if is_home_page != 1:
                    weibo_rows.append([username, text[0], weibo_time[0], users[1], text[1], weibo_time[1]])
                else:
                    weibo_rows.append([users[0], text[0], weibo_time[0], users[1], text[1], weibo_time[1]])
                
    #find all href in the page
        if is_home_page == 1:
            for each_href in browser.find_elements_by_xpath('//a[@class="W_f14 W_fb S_txt1"]'):
                href_url = each_href.get_attribute('href')
                href_user_name = each_href.get_attribute('nick-name')
                
                if href_url not in href_user_dict.keys():
                    href_user_dict[href_url] = href_user_name
                    
        for each_href in browser.find_elements_by_xpath('//a[@class="W_fb S_txt1"]'):
            href_url = each_href.get_attribute('href')
            href_user_name = each_href.get_attribute('nick-name')
            
            if href_url not in href_user_dict.keys():
                href_user_dict[href_url] = href_user_name
        
        if nextpage_button is None:
            print(browser.current_url, "didn't exhaust all page")
            break
        elif page_num < n_page-1:
            
            browser.get(nextpage_button)
    
    return href_user_dict



def weibo_crawl(href_url_dict, depth_limit, expect_date):
    global depth, weibo_href
    depth += 1
    for each_url in href_url_dict.keys():
        if each_url not in weibo_href:
            weibo_user = href_url_dict[each_url]
            weibo_href.add(each_url)
            next_depth_href = collect_weibo(expect_date,each_url,0,weibo_user)
            if next_depth_href is None:
                continue
            else:
                if depth < depth_limit: #limit depth to avoid huge loop
                    weibo_crawl(next_depth_href,depth_limit,expect_date)


browser=webdriver.PhantomJS('phantomjs')
browser.set_window_size(1125, 550)
browser.get("http://weibo.com")
wait = ui.WebDriverWait(browser,10)
sleep(15)
login(user,psw)
sleep(5)
print(browser.current_url)

weibo_rows = []
weibo_href = set()
pagenum_check = re.compile('countPage=([0-9]*)')

expect_date = datetime.strptime("2015-09-04 7:00", '%Y-%m-%d %H:%M')
follow_href = collect_weibo(expect_date,homepage,1)
start_time = time.time()

depth = 0
weibo_crawl(follow_href,depth_limit=5,expect_date)

#print(weibo_rows)


