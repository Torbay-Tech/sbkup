import os
import json
import requests
import time
import sys
from datetime import datetime
import lib.logging as logging
import lib.readCfg as readCfg
import lib.core.listChannels as lc
import lib.core.downloadChannel as dc
import lib.core.userslist as ul



log = logging.getLogger(__file__)
log.info("Loading Backup Main")


def executeBackup():
    # STEP1: Check if Auth token is valid
    # STEP1.A: Download the users list
    # STEP2: List the channel ID's
    # STEP2.A: Add the app to the Channels
    # STEP3: Download each Channel into its own folder
    
    import lib.core.authtest as authtest
    log.info("Initiating Step 1: Auth Test")
    if authtest.testAuth():
        log.info("Auth Test was successful")
    else:
        log.error("Auth Test Failed- check authnetication token permissions")
        sys.exit()
    log.info ("Initializing Step  1 A : Download users")
    ul.loadusers()
    log.info("Initiating Step 2: Get Channels list")
    clist= lc.getChannelList()
    log.info(f"There are {len(clist)} channels that are returned")

    log.info("Starting Step 3: channels conversation backup")
    for c in clist:
      log.info(f"Starting download for channel : {c['name']}")
      #if c['name'] == 'secureme': ## REMOVE THIS - ADDED FOR TESTING ONLY
      dc.downloadConversation(c)
    log.info("Back up Completed for all channels")
    
    

