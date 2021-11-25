from loguru import logger

logger.add(f"logs/errors.log", format="{time} {level} {message}", level="ERROR")
logger.add(f"logs/info.log", format="{time} {level} {message}", level="INFO")
