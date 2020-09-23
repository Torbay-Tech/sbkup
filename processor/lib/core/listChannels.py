import requests
import json
import time
import lib.logging as logging
import lib.readCfg as readCfg
import lib.utilities as util
log = logging.getLogger(__file__)
log.info("Loading List Channels")

def getChannelList():
    clist = []
    log.info("Initializing Get Channels List")
    config = readCfg.read_config(['config/application.properties'])
    conv_list_value = config.get('slack','u_conversations_list')
    log.debug(f"Got the auth URL as {conv_list_value}")
    # First replace the token in the URL with valid token
    conv_list_url = util.updateURLToken(conv_list_value)
    convurl = conv_list_url
    continued = True
    while continued:   
        resp = requests.get(url=convurl)
        log.info(f"Status code returned is: {resp.status_code}")
        rjson = resp.json()
        log.debug(f"The response received is : \n{json.dumps(rjson,indent=4)}")
        channelsArray = rjson['channels']
        log.debug(f"Number of channels is: {len(channelsArray)}")
        #Iterate through channel and add that to clist array
        for c in channelsArray:
            cobj = {}
            cobj['id'] = c['id']
            cobj['name'] = c['name']
            cobj['is_private'] = c['is_private']
            clist.append(cobj)

        # Check if there are more channels
        nxtCursor = rjson['response_metadata']['next_cursor']
        # cursor is returned but empty whn no more present- so lets check length
        if len(nxtCursor) > 2:
            log.debug(f"Next Cursor returned is :{nxtCursor} - more channels present")
            convurl = conv_list_url+"&cursor="+nxtCursor
            time.sleep(2)
        else:
            log.debug("No more channels ")
            continued = False
    log.debug(clist)
    return clist   
    
    