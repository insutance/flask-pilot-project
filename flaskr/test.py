'''
from datetime import datetime

time = datetime.now()

print("현재시간" + time.strftime("%Y-%m-%d %p %H:%M:%S"))
'''

 n = 0
            data = {}

            while n<=10:
                n = n + 1

                news_title = soup.select_one('#sp_nws'+ str(n) +' > dl > dt > a')
                news_url = soup.select_one('#sp_nws'+str(n)+' > dl > dd.txt_inline > a')    #네이버 뉴스 링크

                if news_title is None:
                    print('제목 continue')
                    continue
                
                if news_url is None:
                    print("언론사 continue")
                    continue
                
                data[news_title.text] = news_url.get('href')
        
            for key, value in data.items():
                searchedData = SearchedData(searched_news_title=key, searched_news_url=value, searched_news_time=datetime.now())
                db.session.add(searchedData)
                db.session.commit()

