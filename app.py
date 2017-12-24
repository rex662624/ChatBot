import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine

#抓取ngork網址(curl要安裝在D:\curl)
import json
import os 

os.system("D:\curl\curl  http://localhost:4040/api/tunnels > tunnels.json")

with open('tunnels.json') as data_file:    
    datajson = json.load(data_file)


for i in datajson['tunnels']:
  url =  i['public_url']
  if url[4]=='s':
      break;
  
#########################################
    
API_TOKEN = '471395993:AAEgizhXCIKXbJuspQ6m1QP7lnmdSmo1kXA'
WEBHOOK_URL = url+'/hook'#這行設定URL 原來:'https://c82a342d.ngrok.io/hook'
#WEBHOOK_URL = 'https://c82a342d.ngrok.io/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'prestart',
        'start',
        'avengers',
        'newmovie',
        'Iron_man',
        'thor',
        'captain',
        'movie1',
        'trailer1',
        'lottery',
        'lottery_again'
    ],
    transitions=[
        {#到Start
            'trigger': 'advance',
            'source': 'prestart',
            'dest': 'start',
            
        },
       ###########談論電影##################
        
         
        {
            'trigger': 'advance',
            'source': 'start',
            'dest': 'avengers',
            'conditions': 'go_to_avengers'
        },
        
        {
            'trigger': 'advance',
            'source': 'avengers',
            'dest': 'Iron_man',
            'conditions': 'go_to_Iron_man'
        },
        {
            'trigger': 'advance',
            'source': 'avengers',
            'dest': 'captain',
            'conditions': 'go_to_captain'
        },
        {
            'trigger': 'advance',
            'source': 'avengers',
            'dest': 'thor',
            'conditions': 'go_to_thor'
        },
        {
            'trigger': 'go_back',
            'source': [
		'thor',
                'captain',
                'Iron_man'
                
                
            ],
            'dest': 'start'
        },
        #####最新電影####################
        {
            'trigger': 'advance',
            'source': 'start',
            'dest': 'newmovie',
            'conditions': 'go_to_newmovie'
        },
        
        {
            'trigger': 'advance',
            'source': 'newmovie',
            'dest': 'movie1',
            'conditions': 'go_to_movie1'
        },
        {
            'trigger': 'advance',
            'source': 'movie1',
            'dest': 'trailer1',
            'conditions': 'gotrailer1'
        },
        {
            'trigger': 'advance',
            'source': 'movie1',
            'dest': 'start',
            'conditions': 'movie_no'
        },
        
        {
            'trigger': 'go_back',
            'source':'trailer1',
            'dest': 'start'
        },

        #######電影樂透#######
           
        {
            'trigger': 'advance',
            'source': 'start',
            'dest': 'lottery',
            'conditions': 'go_to_lottery'
        },
        #因為不能source dest都相同 只好讓他前進再無條件回去
        {
            'trigger': 'advance',
            'source': 'lottery',
            'dest': 'lottery_again',
            'conditions': 'lotrery_again'
        },
        {
            'trigger': 'go_back',
            'source': 'lottery_again',
            'dest': 'lottery',
        },
        
        {
            'trigger': 'advance',
            'source': 'lottery',
            'dest': 'start',
            'conditions': 'lottery_exit'
        }
       
        
    ],
    initial='prestart',
    auto_transitions=False,
    show_conditions=True,
)

    


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run()
