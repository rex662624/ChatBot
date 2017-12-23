from transitions.extensions import GraphMachine
import re
import requests
from bs4 import BeautifulSoup
import sys
import shutil

import random

movie = "現正熱映:\n\n" #存放電影清單(global)
picture = [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "]
trailer = [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "]
judge = 0;      #不要重複爬蟲
string = " "#輸入進找trailer的
index = -1 #目前電影的編號

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def on_enter_start(self, update): #一開始start 的輸出文字
            update.message.reply_text("Hi ,I'm a Movie bot\n\n1. You can ask me about the newest moive.\n\n2.You can get a movie by lottery.\n\n3.Or you  talk about my favorite movie \"Marvel's The Avengers\"\n")
###電影樂透############################################
    def go_to_lottery(self, update):#進樂透機
        text = update.message.text
        return text.lower() == 'lottery'
    def on_enter_lottery(self, update):#隨機推薦一個電影 從txt檔中
        file = open("movie.txt","r")
        i = random.randint(1,786)#總共有786個電影
        for j in range(i-1):#從0~i-1是不要的
            file.readline()
        update.message.reply_text(file.readline())
        
    def lotrery_again(self, update):#再一次
        text = update.message.text
        return text.lower() == 'again'
    
    def on_enter_lottery_again(self, update):
        self.go_back(update)
    
    def lottery_exit(self, update):#跳出樂透
        text = update.message.text
        return text.lower() == 'exit'
    
        
###復仇者聯盟##########################################
    def go_to_avengers(self, update):#談論電影
        text = update.message.text
        return text.lower() == 'avengers'
    
    def on_enter_avengers(self, update):
        update.message.reply_text("The Avengers is a Cool movie,which hero is your favorite?")
        
    def go_to_Iron_man(self, update):#Iron man
        text = update.message.text
        return text.lower() == 'iron man'
    
    def on_enter_Iron_man(self, update):
        update.message.reply_text("He is funny and cool.")
        update.message.reply_video('https://media.giphy.com/media/xUOxffaFE2MNvbENa0/giphy.gif')
        self.go_back(update)
        
    def go_to_captain(self, update):#captain
        text = update.message.text
        return text.lower() == 'captain'
    
    def on_enter_captain(self, update):
        update.message.reply_text("He is strong and brave.")
        update.message.reply_video('https://media.giphy.com/media/3ohc0Z1Jn7ZgeDcQ1y/giphy.gif')
        self.go_back(update)
        
    def go_to_thor(self, update):#thor
        text = update.message.text
        return text.lower() == 'thor'
    
    def on_enter_thor(self, update):
        update.message.reply_text("He is also my favorite hero.")
        update.message.reply_video('https://media.giphy.com/media/3oFzmfWhgxWEFRsztu/giphy.gif')
        self.go_back(update)


        
#####最新電影##########################################
    def go_to_newmovie(self, update):#最新電影
        text = update.message.text
        return text.lower() == 'newmovie'

    #####爬蟲抓取新電影
     
    def on_enter_newmovie(self, update):
        global judge
        n = judge #如果不這樣會 UnboundLocalError: local variable 'judge' referenced before assignment
        if(n ==0):#如果剛才沒爬過(不要重複爬蟲)
        
            html_page =requests.get('http://www.3d-movies.tw/').text.splitlines()
            j = 0
            global html_page
            # print(len(html_page)) 網頁的行數
            for i in range(0,len(html_page)):    #擷取原始碼的行數 從第0行到最後一行
            
                if "<td height=\"55\" align=\"left\" valign=\"top\" class=\"s04\" >"  in html_page[i]:
                    global movie 
                    movie   =  (movie +"*"+str(j+1)+". " +html_page[i][99:-5]+"\n")  # 1. XXXXXXX \n ("*"+i+". "+ movie + html_page[i][99:-5]+"\n")
                    trailer[j] = html_page[i][99:-5]    #把所有電影名稱存進去
                     
                    if j==7 :
                        movie  = movie + "\n近期上映:\n\n"
                    #先把圖片網址存進array
                    if j <8 :
                        global picture 
                        picture[j]= ("http://www.3d-movies.tw/"+html_page[i-3][174:-31])#圖片
                        print(picture[j])
                    else:
                        global picture 
                        picture[j]= ("http://www.3d-movies.tw/"+html_page[i-3][174:-30])#圖片
        
                    j+=1
                
        judge = 1                
        update.message.reply_text(movie)
        
    def go_to_movie1(self, update):#最新電影
        text = update.message.text
        ret =((text.lower() == '1')|(text.lower() == '2')|(text.lower() == '3')|(text.lower() == '4')|\
              (text.lower() == '5')|(text.lower() == '6')|(text.lower() == '7')|(text.lower() == '8')|\
              (text.lower() == '9')|(text.lower() == '10')|(text.lower() == '11')|(text.lower() == '12')|\
              (text.lower() == '13')|(text.lower() == '14')|(text.lower() == '15')|(text.lower() == '16'))
               #如果是輸入1~16是合法 給圖片並問是否要看預告片
        if ret==1 :
            global index
            index = int(text.lower())-1 #把input string 轉成int,-1才是真的index
        
        return ret
        
    def on_enter_movie1(self,update):#送出電影圖片
        global index
        update.message.reply_photo(picture[index])
        update.message.reply_text("Want to watch trailer ?")
        
    def movie_no(self, update):#不要看預告片 回到Start
        text = update.message.text
        return text.lower() == 'no'

    def gotrailer1(self, update):#要看預告片
        text = update.message.text
        return text.lower() == 'yes'
            
    
    def on_enter_trailer1(self,update):
        global string
        global index
        string = trailer[index]
        update.message.reply_text(findtrailer())
        self.go_back(update)

        
def findtrailer():
    global string
    url = "https://www.youtube.com/results?search_query=" + string
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text,'html.parser')
    last = None
    for entry in soup.select('a'): #篩選是a標籤 的元素
        m = re.search("v=(.*)",entry['href'])
        #去找超連結的group <a href> ,https://www.youtube.com/watch?v=[hash值]
        
        if m:
            return("https://www.youtube.com/watch?"+m.group())#找到的第一個return             
   
        
    
    
 
