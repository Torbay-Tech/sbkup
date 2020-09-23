import os
import json
import requests
import time
import sys
from datetime import datetime
import lib.logging as logging
import lib.readCfg as readCfg
import lib.utilities as util
from pathlib import Path

CHANNELS_PATH = "data/html/channels/"
HTML_PATH = 'data/html/'
log = logging.getLogger(__file__)
log.info("Loading download Channel")

def getdisplayTime(messagets):
    tsa = messagets.split(".")
    ts = int(tsa[0])
    sentdt = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return sentdt

def updateRawFile(path,msg, mode='a+t'):
    with open (path, mode) as rf:
        rf.write(msg)
        rf.close()

def downloadFile(downloadurl, filename, channelname ):
    log.debug("Downloading file")
    token= util.getAuthToken()
    bearertoken = 'Bearer '+token
    headers = {
        'Authorization': bearertoken
    }
    fresp = requests.get(url=downloadurl, headers = headers)
    log.debug(f"Response code returned is :{fresp.status_code} for file {filename}")
    file_data = fresp.content
    filename = CHANNELS_PATH+channelname+"/"+filename    
    fn = Path(filename)
    fn.write_bytes(file_data)
    time.sleep(2)

def parseMessages(msgs, channelname):
    for m in msgs:
        if "files" in m:
            log.debug("This message is a file ")
            durl = m['files'][0]['url_private']
            dname = m['files'][0]['name']
            did = m['files'][0]['id']
            dmime = m['files'][0]['mimetype']
            dname = did+"_"+dname
            log.debug(f"File name is : {dname} and mime type is {dmime}")
            downloadFile(downloadurl=durl, filename=dname, channelname=channelname)
        elif "client_msg_id" in m:
            log.debug("This message is a text message ")
            messagesender = translateuser(m['user'])
            messagets= m['ts']
            tsa = messagets.split(".")
            ts = int(tsa[0])
            sentdt = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            log.debug(f"Text message sent at {sentdt} by {messagesender}")
            #print(m['text'])
        else:
            log.debug("Not a file or text message:")
            log.debug(json.dumps(m,indent=4))
def downloadConversation(channel):
    chpath = CHANNELS_PATH+channel['name']
    rawfilepath = chpath+"/raw.json"
    if os.path.exists(HTML_PATH) == False:
        os.mkdir(HTML_PATH)
        #create the HTML folder
    if os.path.exists(CHANNELS_PATH) == False:
        os.mkdir(CHANNELS_PATH)
        #create the channels base folder
    if os.path.exists(chpath) == False:
        os.mkdir(chpath)
        #create the folder for individual channel
    else:
        os.remove(rawfilepath)
        #VClean up the raw file 
    
    config = readCfg.read_config(['config/application.properties'])
    u = config.get('slack','u_conversations_history')
    conv_hist_url = util.updateURLToken(u)
    u = util.updateURLChannel(url=conv_hist_url,channelname=channel['id'])
    #channel_path = chpath+"/"
    continued = True
    channelmsgs = []
    cm= {}
    newu = u
    while continued:
        resp = requests.get(url=newu)
        log.debug(f"Status returned  is: {resp.status_code}")
        rjson = resp.json()
        log.debug(f"Message returned is \n {json.dumps(rjson,indent=4)}")
        try:
            msgs =  rjson['messages']
            for a in msgs:
                channelmsgs.append(a)
        except KeyError:
            log.info(f"No messages OR Not member of channel: {channel['name']}")
            updateRawFile(path=rawfilepath,msg=json.dumps(rjson, indent=4),mode='w+t')
            return
        parseMessages(msgs,channel['name'])
        continued = rjson['has_more']
        #continued = False # Added for testing REMOVE THIS
        if continued:
            nxtCursor = rjson['response_metadata']["next_cursor"]
            log.info(f"Response paginated- continuing with cursor: {nxtCursor}")
            time.sleep(2)
            newu = u + "&cursor="+nxtCursor
        else:
            cm['messages']=channelmsgs
            updateRawFile(path=rawfilepath,msg=json.dumps(cm,indent=4))
            log.info(f"Completed retriveing all converstions for the channel: {channel['name']}")