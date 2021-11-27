from loguru import logger


logger.add('debug.log', format='{time} {message}', rotation='1 week', compression='zip')
