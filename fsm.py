from transitions.extensions import GraphMachine
from utils import send_text_message
from utils import send_image_url
from bs4 import BeautifulSoup

import re
import requests
import random
import datetime

dest_url = ""
comb = ""

picture = ["https://i.imgur.com/bVAE9Ou.jpg",
           "https://i.imgur.com/DDHvm6h.png",
           "https://i.imgur.com/7T4X7aV.png",
           "https://i.imgur.com/zNfOpO1.png",
           "https://i.imgur.com/MB9mVYo.png"
          ]

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
        model=self,
        **machine_configs
    )

    def is_going_to_stateNBA(self, event):
        if (event.get("message")) and ((event.get("message")).get("text")):
            target_str = "NBA"
            text = event['message']['text']
            #print((text.lower().find(target_str.lower())) != -1)
            return (text.lower().find(target_str.lower())) != -1
	
        return False

    def is_going_to_stateGame(self, event):
        if (event.get("message")) and ((event.get("message")).get("text")):
            target_str = "比賽結果" 
            text = event['message']['text']
            return text.find(target_str) != -1
        return False
    
    def is_going_to_stateResult(self, event):
        if (event.get("message")) and ((event.get("message")).get("text")):
            check_str = "Please enter team name to see game result"
            text = event['message']['text']
            return text.find(check_str) == -1
        return False

    def is_going_to_stateScoreboard(self, event): 
        if (event.get("message")) and ((event.get("message")).get("text")):
            target_str = "數據" 
            text = event['message']['text']
            return text.find(target_str) != -1
        return False

    def is_going_to_stateHighlight(self, event): 
        if (event.get("message")) and ((event.get("message")).get("text")):    
            target_str = "highlight" 
            text = event['message']['text']
            return text.lower().find(target_str.lower()) != -1
        return False

    def is_going_to_stateMusic(self, event): 
        if (event.get("message")) and ((event.get("message")).get("text")):
            target_str = "音樂" 
            text = event['message']['text']
            return text.find(target_str) != -1
        return False

    def is_going_to_stateSearchMusic(self, event): 
        if (event.get("message")) and ((event.get("message")).get("text")):
            check_str = "For user input"
            text = event['message']['text']
            return text.find(check_str) == -1
        return False
    
    def is_going_to_stateVideo(self, event):
        if (event.get("message")) and ((event.get("message")).get("text")):
            target_str = "影片"
            text = event['message']['text']
            return text.find(target_str) != -1
        return False

    def is_going_to_stateSearchVideo(self, event): 
        if (event.get("message")) and ((event.get("message")).get("text")):
            check_str = "For user input"
            text = event['message']['text']
            return text.find(check_str) == -1
        return False
    
    def is_going_to_stateLuck(self, event):
        if (event.get("message")) and ((event.get("message")).get("text")):
            target_str = "運勢" 
            text = event['message']['text']
            return text.find(target_str) != -1
        return False

    
    def on_enter_user(self):
        print("I'm returning to state user")

    def on_enter_stateNBA(self, event):
        
        sender_id = event['sender']['id']

        url = "https://sports.yahoo.com/nba/scoreboard/"
        res = requests.get(url, verify = False)
        soup = BeautifulSoup(res.text, 'html.parser')
        game_list = soup.find('ul', class_= 'Mb(0px)').find_all('div', class_= 'Px(20px) Py(10px)')
        
        msg = "NBA Games Today:\n\n"
        for game in game_list:
            last_name = game.find_all('div', class_= 'Fw(n) Fz(12px)')
            msg = msg + last_name[0].string + " vs " + last_name[1].string + "\n"

        responese = send_text_message(sender_id, msg)     
        
    def on_enter_stateGame(self, event):
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "Please enter team name to see game result")

    def on_enter_stateResult(self, event):
       
        sender_id = event['sender']['id']
        
        if (event.get("message")) and ((event.get("message")).get("text")):
        
            text = event['message']['text']
            src_url = "https://sports.yahoo.com/nba/scoreboard/"
            src_res = requests.get(src_url, verify = False)
            src_soup = BeautifulSoup(src_res.text, 'html.parser')

            top_list = src_soup.find('ul', class_= 'Mb(0px)')
            game_list = top_list.find_all('div', class_= 'Px(20px) Py(10px)')
            box_list = top_list.find_all('a', class_= 'C(primary-text) C(primary-text):link C(primary-text):visited Td(n) gamecard-final') 

            name_flag = False        
            for game in game_list:
                first_name = game.find_all('div', class_= 'Fw(b) Fz(14px)')
                last_name = game.find_all('div', class_= 'Fw(n) Fz(12px)')
                away_first = first_name[0].find('span').string
                away_last = last_name[0].string
                away_name = away_first + " " + away_last
                home_first = first_name[1].find('span').string
                home_last = last_name[1].string
                home_name = home_first + " " + home_last
                if ((away_name.lower()).find(text.lower()) != -1) or ((home_name.lower()).find(text.lower()) != -1):
                    name_flag = True
                    break

            global dest_url
            dest_flag = False
            for entry in box_list:
                if (entry['href'].lower()).find(text.lower()) != -1:
                    dest_flag = True
                    dest_url = entry['href']
                    break

            if (name_flag == True) and (dest_flag == True):

                global comb
                dest_url = "http://sports.yahoo.com" + dest_url
                dest_res = requests.get(dest_url, verify = False)
                dest_soup = BeautifulSoup(dest_res.text, 'html.parser')

                away_score_list = dest_soup.find_all('span',class_= "Fz(48px) D(b) My(0px) Lh(56px) Or(3) Fw(500) Ta(end) Px(10px)")
                away_score = away_score_list[0].contents[1]
                home_score_list = dest_soup.find_all('span',class_= "Fz(48px) D(b) My(0px) Lh(56px) Or(3) Fw(500) Ta(start) Px(10px)")
                home_score = home_score_list[0].contents[1]

                comb = away_last + " vs " + home_last
                responese = send_text_message(sender_id, away_last + " " + away_score + " : " + home_score + " " + home_last)

            elif name_flag == True:
                responese = send_text_message(sender_id, "This game has not finished!")
            else:
                responese = send_text_message(sender_id, "This game can't be found!")
                    
    
    def on_enter_stateHighlight(self, event):
        sender_id = event['sender']['id']
        result_list = Search_Youtube(comb + " highlight", 1)
        responese = send_text_message(sender_id, result_list[0])
        self.go_back()

    def on_enter_stateScoreboard(self, event):
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, dest_url)
        self.go_back()

    def on_enter_stateMusic(self, event):
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "For user input")     

    def on_enter_stateSearchMusic(self, event):
        sender_id = event['sender']['id']
        if event.get("message"):
            text = event['message']['text']
            result_list = Search_Youtube(text, 1)
            responese = send_text_message(sender_id, result_list[0])
        self.go_back()
     
    def on_enter_stateVideo(self, event):
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "For user input")

    def on_enter_stateSearchVideo(self, event):
        sender_id = event['sender']['id']
        if event.get("message"):
            text = event['message']['text']
            result_list = Search_Youtube(text, 3)
            for url in result_list:
                responese = send_text_message(sender_id, url)
        self.go_back()

    def on_enter_stateLuck(self, event):
        sender_id = event['sender']['id']
        n = random.randint(0,24)
        pic_num  = 0
        if n >= 22:
            pic_num = 0
        elif (n < 22) and (n >= 16):
            pic_num = 1
        elif (n < 16) and (n >= 5):
            pic_num = 2
        elif n > 0:
            pic_num = 3
        else:
            pic_num = 4

        #responese = send_text_message(sender_id, "I'm entering stateLuck")
        responese = send_image_url(sender_id, picture[pic_num])
        self.go_back()


def Search_Youtube(target, num):
    url = "https://www.youtube.com/results?search_query=" +target
    res = requests.get(url, verify = False)
    soup = BeautifulSoup(res.text, 'html.parser')
    prev = None
    cnt = 0

    result_list = []
    for entry in soup.select('a'):
        item = re.search("v=(.*)", entry['href'])
        if item:
            cur = item.group(1)
            if cur == prev:
                continue
            if re.search("list",cur):
                continue
            prev = cur
            cnt = cnt + 1
            result_list.append("https://www.youtube.com/watch?v=" + cur)
            if cnt >= num:
                break

    return result_list

