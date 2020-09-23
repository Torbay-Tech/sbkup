import os
import json
import requests
import time
import sys
from datetime import datetime
import lib.logging as logging
import lib.readCfg as readCfg
import lib.utilities as util

log = logging.getLogger(__file__)
log.info("Loading download Channel")
config = readCfg.read_config(['config/application.properties'])

def updateUserFile(msg):
    with open ("data/userlist.json", 'a+t') as rf:
        rf.write(msg)
        rf.close()

def loadusers():
    log.info("Loading users list")
    try:
        os.remove("data/userlist.json")
    except:
        log.debug("File not present lets continue")
    u = config.get('slack','u_users_list')
    u = util.updateURLToken(u)
    continued = True
    newu = u
    mlist= []
    while continued:
        resp = requests.get(url=newu)
        log.debug(f"Status returned  is: {resp.status_code}")
        rjson = resp.json()
        log.debug(f"Message returned is \n {json.dumps(rjson,indent=4)}")
        membersArray = rjson['members']
        log.debug(f"Number of members is: {len(membersArray)}")
        #Iterate through memebers and add that to mlist array
        for m in membersArray:
            mobj = {}
            mobj['id'] = m['id']
            mobj['name'] = m['name']
            mobj['profile'] = m['profile']
            mlist.append(mobj)
            
         # Check if there are more users
        nxtCursor = rjson['response_metadata']['next_cursor']
        # cursor is returned but empty whn no more present- so lets check length
        if len(nxtCursor) > 2:
            log.debug(f"Next Cursor returned is :{nxtCursor} - more users present")
            newu = u+"&cursor="+nxtCursor
            time.sleep(2)
        else:
            log.debug("No more users ")
            updateUserFile(json.dumps(mlist,indent=4))
            continued = False

