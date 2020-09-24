import os
import json
import requests
import time
from datetime import datetime
from lib.logging import Logger
from lib.readCfg import ConfigReader
from lib.utilities import Utilities

logging = Logger()
log = logging.getLogger(__file__)
class AuthTest:    
    def __init__(self):
        log.info("Initializing")

    def updateRawFile(self,msg):
        with open ("processor/data/authtest.json", 'w+t') as rf:
            rf.write(msg)
            rf.close()

    def testAuth(self):
        readCfg = ConfigReader()
        config = readCfg.read_config(['processor/config/application.properties'])
        auth_test_value = config.get('slack','u_auth_test')
        log.debug(f"Got the auth URL as {auth_test_value}")
        util = Utilities()
        auth_test_url = util.updateURLToken(auth_test_value)

        # CHECK TOKEN WITH AUTH TEST
        resp = requests.get(url=auth_test_url)
        log.info(f"Status code returned is: {resp.status_code}")
        log.info(resp)
        print(resp)
        rjson = resp.json()
        log.debug(f"The response received is : \n{json.dumps(rjson,indent=4)}")
        # SAVE RESULTS TO authtest.results file
        self.updateRawFile(json.dumps(rjson,indent=4))
        time.sleep(1)
        return True