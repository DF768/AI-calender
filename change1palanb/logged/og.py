import logging
from datetime import datetime

def setup_logger():
    logger = logging.getLogger("calendar_app")
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # 控制台日志
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    # 文件日志
    log_file = f"logs/calendar_{datetime.now().strftime('%Y%m%d')}.log"
    fh = logging.FileHandler(log_file)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    return logger

logger = setup_logger()