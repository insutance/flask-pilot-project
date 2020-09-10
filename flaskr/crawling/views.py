"""
flaskr/crawling/views.py
"""
from flaskr import app, db
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime
from flaskr.models import User, Data, SearchedData
from flaskr.decorator import session_check
import simplejson as json

from bs4 import BeautifulSoup
from selenium import webdriver

"""search"""
@app.route('/search', methods=['POST'])
@session_check
def search():
    if request.method == 'POST':
        print(datetime.now())
        db.session.query(SearchedData).delete()
        db.session.commit()

        #keyword = request.form['inputSearch']
        json_data = request.get_json()

        if json_data['keyword'] == '':
            return jsonify(result="fail"), 400
        
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")

        driver = webdriver.Chrome('/Users/insutance/Downloads/chromedriver', options=options)
        driver.get("https://search.naver.com/search.naver?where=news&sm=tab_jum&query=" + json_data['keyword'])

        page_count = 0
        try:    # 몇페이지까지 있는지 확인 (최대 10page)
            if driver.find_elements_by_xpath('//*[@id="main_pack"]/div/div[2]/strong'):
                page_count += 1
                for i in range(1,3):   # 최대 10페이지, 버튼을 찾을때마다 page_count를 +1 해줌으로써 최대 10페이지까지 찾는다.
                    if driver.find_elements_by_xpath('//*[@id="main_pack"]/div/div[2]/a['+ str(i) +']'):
                        page_count += 1
                    else:
                        break
        except:
            print('몇 페이지 있는지 찾는 부분 오류')

        try:    # page_count 만큼 반복문을 통해 html 변수에 저장
            if page_count > 0:
                html = driver.page_source
                if page_count > 1:
                    # 2page 는 마지막에 '1' 이 들어가서 따로 빼줌.
                    element = driver.find_elements_by_xpath('//*[@id="main_pack"]/div/div[2]/a[1]')
                    element[0].click()
                    html += driver.page_source

                    for i in range(3,page_count+1): # 3page부터는 for문을 통해 
                        if i < 6:
                            element = driver.find_elements_by_xpath('//*[@id="main_pack"]/div/div[2]/a['+ str(i) +']')
                            element[0].click()
                            html += driver.page_source
                        else:
                            element = driver.find_elements_by_xpath('//*[@id="main_pack"]/div/div[2]/a[6]')
                            element[0].click()
                            html += driver.page_source
        except:
            print('크롤링하는 부분 오류')

        driver.quit()   # driver 종료

        try:    # 찾아낸 html을 통해 찾고 싶은 데이터를 DB에 저장
            soup = BeautifulSoup(html, 'html.parser')

            search_naver = soup.select('#main_pack > div.news.mynews.section._prs_nws > ul > li > dl')
            for i in search_naver:
                if i.select_one('dd.txt_inline > a'):
                    title = i.select_one('dt > a').text
                    url = i.select_one('dd.txt_inline > a').get('href')
                    
                    searchedData = SearchedData(searched_news_title=title, searched_news_url=url, searched_news_time=datetime.now())
                    db.session.add(searchedData)
                    db.session.commit()

            datas = SearchedData.query.all()
            data_list = []
            for data in datas:
                data_list.append(data.get_json())
            
            #return redirect(url_for('post', page=1))
            return jsonify(result = "sucess", datas = data_list)
            
        except UnboundLocalError:   # BeautifulSoup(html, 'html.parser') 부분에서 / html 이 위에서 없으면 local 변수가 없다고 판단됨.
            print("검색결과가 없습니다.")
            flash("검색결과가 없습니다")
            return redirect(url_for('index'))

"""post"""
@app.route('/post/<int:page>')
@session_check
def post(page=None):
    datas = SearchedData.query.all()
    posts = SearchedData.query.order_by(SearchedData.searched_news_time.desc()).paginate(page, 3, error_out=False)
    return render_template('post.html', posts = posts, datas_length=len(datas))
    
"""store"""
@app.route('/store', methods=['POST'])
@session_check
def store():
    if request.method=='POST':
        json_data = request.get_json()
        user = session.get('id')
        searched_data = SearchedData.query.filter_by(searched_news_id = json_data['index']).first()
        data = Data(news_title=searched_data.searched_news_title, news_url=searched_data.searched_news_url, 
                            stored_time=datetime.now(), user_id=user)
        db.session.add(data)
        db.session.commit()

        return jsonify(result = "success")