import os
import json
import requests
import time
import sys
from datetime import datetime
from lib.core.authtest import AuthTest
from lib.logging import Logger
#import lib.readCfg as readCfg
#import lib.core.listChannels as lc
from lib.core.downloadChannel import DownloadChannel
from lib.core.userslist import UsersList
from lib.core.authtest import AuthTest
from lib.core.listChannels import ListChannels
from lib.core.htmlgenerator import HtmlGenerator

logging = Logger()
log = logging.getLogger(__file__)
class Backup:
    def __init__(self):
        log.info("Loading Backup Main")

    def executeBackup(self):
        # STEP1: Check if Auth token is valid
        # STEP1.A: Download the users list
        # STEP2: List the channel ID's
        # STEP2.A: Add the app to the Channels
        # STEP3: Download each Channel into its own folder
        # STEP4: Create a HTML conversation view
        
        log.info("Initiating Step 1: Auth Test")
        authtest = AuthTest()
        if authtest.testAuth():
            log.info("Auth Test was successful")
        else:
            log.error("Auth Test Failed- check authentication token permissions")
            sys.exit()
        
        log.info ("Initializing Step  1 A : Download users")
        ul = UsersList()
        ul.loadusers()
        log.info("Initiating Step 2: Get Channels list")
        lc = ListChannels()
        clist= lc.getChannelList()        
        log.info(f"There are {len(clist)} channels that are returned")
        log.info("Starting Step 3: channels conversation backup")
        dc = DownloadChannel()
        for c in clist:
            log.info(f"Starting download for channel : {c['name']}")
            #if c['name'] == 'condonuityleads': ## REMOVE THIS - ADDED FOR TESTING ONLY
            dc.downloadConversation(c)
        log.info("Back up Completed for all channels")

        log.info("Starting Step 4 : Create a HTML Conversation view")      
        
        hg = HtmlGenerator() 
        hg.generateHtmlView()
        

