import lib.logging as logging
import lib.readCfg as readCfg
import sys

log = logging.getLogger(__file__)
log.info("Initializing")
config = readCfg.read_config(['config/secret.properties'])

def updateURLToken(url):    
    authkey = config.get('slack','authkey')
    if authkey == None:
        log.error("Cannot Proceed Auth key Missing in properties")
        sys.exit()
    nurl = url.replace('^^TOKEN^^', authkey)
    return nurl

    
def updateURLChannel(url,channelname):    
    log.debug(f"Updating Channel name in URL to : {channelname}")
    nurl = url.replace('^^CHANNEL^^', channelname)
    return nurl

def getAuthToken():
    log.debug("Requested Auth token")
    return config.get('slack','authkey')
