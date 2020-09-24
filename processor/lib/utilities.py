from lib.logging import Logger
from lib.readCfg import ConfigReader
import sys

logging = Logger()
log = logging.getLogger(__file__)
readCfg= ConfigReader()
config = readCfg.read_config(['processor/config/secret.ini'])
class Utilities:
    def __init__(self):
        log.info("Initializing")
    def updateURLToken(self,url):    
        authkey = config.get('slack','authkey')
        if authkey == None:
            log.error("Cannot Proceed Auth key Missing in properties")
            sys.exit()
        nurl = url.replace('^^TOKEN^^', authkey)
        return nurl

        
    def updateURLChannel(self,url,channelname):    
        log.debug(f"Updating Channel name in URL to : {channelname}")
        nurl = url.replace('^^CHANNEL^^', channelname)
        return nurl

    def getAuthToken(self):
        log.debug("Requested Auth token")
        return config.get('slack','authkey')
