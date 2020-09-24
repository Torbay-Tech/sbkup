from lib.logging import Logger
#from lib.readCfg import ReadCfg
from lib.core.backup import Backup

logging = Logger()
log = logging.getLogger(__file__)
log.info("Initializing")
backup = Backup()
backup.executeBackup()


