import os
import json
import requests
import time
from datetime import datetime
import lib.logging as logging
import lib.readCfg as readCfg
import lib.utilities as util

log = logging.getLogger(__file__)
log.info("Initializing")
def updateRawFile(msg):
    with open ("data/authtest.json", 'w+t') as rf:
        rf.write(msg)
        rf.close()

def testAuth():
    config = readCfg.read_config(['config/application.properties'])
    auth_test_value = config.get('slack','u_auth_test')
    log.debug(f"Got the auth URL as {auth_test_value}")
    auth_test_url = util.updateURLToken(auth_test_value)

    # CHECK TOKEN WITH AUTH TEST
    resp = requests.get(url=auth_test_url)
    log.info(f"Status code returned is: {resp.status_code}")
    rjson = resp.json()
    log.debug(f"The response received is : \n{json.dumps(rjson,indent=4)}")
    # SAVE RESULTS TO authtest.results file
    updateRawFile(json.dumps(rjson,indent=4))
    time.sleep(1)
    return True