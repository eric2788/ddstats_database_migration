from log import logger

if __name__ == '__main__':
    logger.info("The Script Is Working.")
    logger.warning("However, you didn't specific a script to run.")
    logger.warning(
        "Please specify a script to run via changing environment variable: MAIN_PY")
