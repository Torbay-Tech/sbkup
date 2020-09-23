import configparser
import os

'''
A Utility that will read the config file provided and allow access 
to the values as name value pairs
Usage :
config = readCfg.read_config(['config/local.properties','somewhereelse/global.properties'])

if config == None:
    log.error("Config files not found")
VALUE_NEEDED = config.get('section_name', 'key_name')

Properties File will look like 

[section_name]
mykey = myvalue

[another_section]
anotherkey = itsvalue
'''


class ConfigReader:
    def read_config(cfg_files):
        if cfg_files != None:
            config = configparser.ConfigParser()

            for i, cfg_files in enumerate(cfg_files):
                if (os.path.exists(cfg_files)):
                    config.read(cfg_files)
        return config
