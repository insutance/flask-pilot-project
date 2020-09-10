from bs4 import BeautifulSoup
from selenium import webdriver

def crawling(keyword):
    driver = webdriver.Chrome('/Users/insutance/Downloads/chromedriver')
    keyword = "아이폰"
    driver.get("https://search.naver.com/search.naver?where=news&sm=tab_jum&query=" + keyword)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    '''
    element = driver.find_elements_by_xpath('//*[@id="main_pack"]/div/div[2]/a[1]')
    element[0].click()

    html2 = driver.page_source
    soup2 = BeautifulSoup(html2, 'html.parser')
    '''
    driver.quit()

    n = 0
    data = {}
    '''
    test = soup.select('#main_pack > div.news.mynews.section._prs_nws > ul > li > dl > dt > a')
    
    for i in test:
        #print(i.text)
    
    test2 = soup.select('#main_pack > div.news.mynews.section._prs_nws > ul > li > dl > dd.txt_inline > a')
    for i in test2:
        if i.text is None:
            #print('none')
        else:
            #print(i.text)
   ''' 
    test3 = soup.select('#main_pack > div.news.mynews.section._prs_nws > ul > li > dl')
    for i in test3:
        if i.select_one('dd.txt_inline > a'):
            title = i.select_one('dt > a').text
            url = i.select_one('dd.txt_inline > a').get('href')
            
            searchedData = SearchedData(searched_news_title=title, searched_news_url=url, searched_news_time=datetime.now())
            db.session.add(searchedData)
            db.session.commit()

    while n<=10:
        n = n + 1

        news_title = soup.select_one('#sp_nws'+ str(n) +' > dl > dt > a')
        news_url = soup.select_one('#sp_nws'+str(n)+' > dl > dd.txt_inline > a')    #네이버 뉴스 링크

        if news_title is None:
            #print('제목 continue')
            continue
        
        if news_url is None:
            #print("언론사 continue")
            continue
        
        data[news_title] = news_url
        #print(data)
    
    return news_titles, news_urls

crawling('아이폰')