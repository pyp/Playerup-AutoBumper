import logging, cfscrape, os, json, time
from time import strftime, gmtime

#made with <3 by doozle#1337 from discord.gg/rozegg

logging.basicConfig(
    level=logging.INFO,
    format=f"\x1b[38;5;61m[\x1b[0m%(asctime)s\x1b[38;5;61m]\x1b[0m -> \x1b[38;5;61m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

class playerup:
    def __init__(self):
        with open("data/config.json", encoding="utf-8") as f: self.config = json.load(f)
        self.session = cfscrape.create_scraper()
        
    def fetchSess(self):
        r = self.session.get('https://playerup.com/', headers={'cookie': self.config['cookie']})
        if r.status_code == 200: 
            logging.info('\x1b[0mFetched playerup session. \x1b[38;5;61m(\x1b[0m%s\x1b[38;5;61m)' % r.text.split('_xfToken" value="')[1].split('"')[0])
            return r.text.split('_xfToken" value="')[1].split('"')[0]
        else: 
            logging.info('\x1b[0mFailed to fetch playerup session. \x1b[0m(\x1b[38;5;61m%s\x1b[0m)' % r.status_code)
                
    def sendBump(self, thread_link: str):
        sess = self.fetchSess()
        r = self.session.post('%s/add-reply' % thread_link, headers={'cookie': self.config['cookie']}, data={'message_html': '<p>%s (%s)</p>' % (self.config['message'], os.urandom(4).hex()), '_xfToken': sess, '_xfRequestUri': thread_link, '_xfNoRedirect': '1', '_xfResponseType': 'json', '_xfToken': sess})
        if self.config['debug']: logging.info('\x1b[0m%s' % r.json())
        if r.status_code == 200: logging.info('\x1b[0mSuccessfully bumped thread. \x1b[38;5;61m(\x1b[0m%s\x1b[38;5;61m)\n' % thread_link)
        else: logging.error('\x1b[0mFailed to bump thread. \x1b[0m(\x1b[38;5;61m%s\x1b[0m)\n' % r.status_code)

    def start(self):
        while True: 
            for thread in self.config['threads']:
                self.sendBump(thread)
                time.sleep(7.5)
                
            retry = self.config['interval']
            for i in range(retry, 0, -1):
                print("\x1b[38;5;61m[\u001b[0m%s\x1b[38;5;61m]\u001b[0m Sleeping for \x1b[38;5;61m%s\u001b[0m seconds.              " % (strftime("%H:%M:%S", gmtime()), i), end="\r")
                time.sleep(1)

os.system('cls')
playerup().start()
