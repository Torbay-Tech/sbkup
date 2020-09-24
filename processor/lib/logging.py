import logging
import os
import sys
from lib.readCfg import ConfigReader
'''
Simple Logger utility
add this line to py file
log = logging.getLogger(__file__)
 and use the log object by calling
log.error("My error message")
log.info("My info message")

'''

class Logger:
    def __init__(self):
        readCfg = ConfigReader()
        config = readCfg.read_config(['processor/config/application.properties'])
        if config == None:
            print("Config files not found")
            sys.exit()

        LOG_FILE_PATH = config.get('common', 'logpath')
        # set up logging to file - see previous section for more details
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            filename=LOG_FILE_PATH, 
                            filemode='w')
        # define a Handler which writes INFO messages or higher to the sys.stderr
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        # tell the handler to use this format
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger('').addHandler(console)

    def getLogger(self,fileName):
        return logging.getLogger(os.path.basename(fileName))