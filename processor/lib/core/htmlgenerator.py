import os
import json
import requests
import time
import sys
from shutil import copyfile
from datetime import datetime
from lib.logging import Logger
from lib.readCfg import ConfigReader
import dominate
from dominate.tags import *
from dominate.tags import link
from dominate.tags import div
from dominate.tags import attr

logging = Logger()
readCfg = ConfigReader()
HTML_PATH = "processor/data/html/"
CHANNELS_PATH = "processor/data/html/channels/"
log = logging.getLogger(__file__)
USER_PATH = 'processor/data/userlist.json'
with open(USER_PATH) as u:
    try:
        userdata = json.load(u)
    except:
        log.error("Ignore as there is no user list")
        userdata= {}


class HtmlGenerator:
    def __init__(self):
        log.info("Loading Backup Main")
        log.info(f"Length of userdata is {len(userdata)}")

    def translateuser(self,userid):
        log.debug(f"Accessing user info for {userid}")
        for user in userdata:
            if user['id'] == userid:
                return user['name']
        return userid

    def getDisplayTime(self,messagets):
        tsa = messagets.split(".")
        ts = int(tsa[0])
        sentdt = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        return sentdt
    def renderChannelPage(self,cpage):
        chdoc = dominate.document(title=cpage)
        log.info(f"Rendering {cpage}")    
        with chdoc.head:
            link(rel='stylesheet', href='css/styles.css')
        with chdoc:
        # Iterate through a loop and create the list of channels
            h3(cpage)
            log.info(f"Creating detailed page for Channel {cpage}")
            rawpath = CHANNELS_PATH+cpage+"/raw.json"
            with open(rawpath) as f:
                data = json.load(f)
            try :
                msgs = data['messages']
            except KeyError:
                log.info("No message found this is OK")
                h3("No message in channel")
                fpath = HTML_PATH+cpage+".html"
                self.updateRawFile(path=fpath,msg=str(chdoc))
                return chdoc
                
            except TypeError:
                log.info("No message found this is OK")
                h3("Type error message in channel")
                fpath = HTML_PATH+cpage+".html"
                self.updateRawFile(path=fpath,msg=str(chdoc))
                return chdoc
                
            for m in msgs:
                try:
                    if "files" in m or 'attachments' in m:
                        #print("This message is a file and the URL is")                    
                        log.debug(f"File name or attachment present ")
                        if 'files' in m:
                            dname = m['files'][0]['name']
                            did = m['files'][0]['id']
                            dname = did+"_"+dname
                            with div(self.translateuser(m['user'])):
                                attr(cls='usern')
                            with div(self.getDisplayTime(m['ts'])):
                                attr(cls='time')
                            with div(dname):
                                attr(cls='files')
                        elif 'attachments' in m:
                            #log.info(f"Attachment:  {m}")
                            log.info(f"Attachments: Title- {m['attachments'][0]['title']} ")#text is {m['text']} user is {m['attachments'][0]['user']} ts is {m['attachments'][0]['ts']}")
                            #ADD ADDING Files to Chat logic
                    elif "user" in m and 'ts' in m and 'text' in m:
                        log.debug(f"Message read is {m['text']} sent by {m['user']} on {m['ts']}")
                        with div(self.translateuser(m['user'])):
                            attr(cls='usern')
                        with div(self.getDisplayTime(m['ts'])):
                            attr(cls='time')
                        with div(m['text']):
                            attr(cls='box1 sb1')
                    elif 'subtype' in m :
                        log.info(f"Channel join or leave message {m}")
                    else:
                        log.info(f"Non client message ")
                except KeyError:
                    log.info(f"One of the keys missing- this is a DEFECT- should not happen {m}")
                    log.error(KeyError)
                    break
                
                    
        ###REMOVE THIS _ FOR TESTING ONLY
        #fpath = HTML_PATH+cpage+".html"
        #updateRawFile(path=fpath,msg=str(chdoc))
        ### REMOVE ABOVE FOR TESTING ONLY

        return chdoc


    def updateRawFile(self,path,msg, mode='w+t'):
        with open (path, mode) as rf:
            rf.write(msg)
            rf.close()
    def generateHtmlView(self):
        log.info("Generating HTML view")
        #lets remove the HTML file if present
        if os.path.exists(HTML_PATH) == False:
            os.mkdir(HTML_PATH)
            os.mkdir(HTML_PATH+"css/")
        rawfilepath = HTML_PATH+"index.html"
        if os.path.exists(HTML_PATH+"css/") == False:
            os.mkdir(HTML_PATH+"css/")
        copyfile('processor/lib/ui/html/css/styles.css','processor/data/html/css/styles.css')
        indexdoc = dominate.document(title="Torbay Slack Chats")
        list_subfolders = [f.name for f in os.scandir(CHANNELS_PATH) if f.is_dir()]
        with indexdoc.head:
            link(rel='stylesheet', href='css/styles.css')
        with indexdoc:
            # Iterate through a loop and create the list of channels
            h3('Channels list')
            log.info("Creating Channels list page")        
            for ch in list_subfolders:
                log.debug(f"Creating Channel entry for {ch}")
                chdisplay = '#'+ch
                chlink = ch+".html"
                with a(href=chlink):
                    with div(chdisplay):
                        attr(cls='channels')    
        log.debug(indexdoc)
        self.updateRawFile(path=rawfilepath,msg=str(indexdoc))
        log.info("Generation of index.html completed")
        # Next step is create the html file for each channel
        for cpage in list_subfolders:
            fpath = HTML_PATH+cpage+".html"
            chdoc = self.renderChannelPage(cpage)
            self.updateRawFile(path=fpath,msg=str(chdoc))

