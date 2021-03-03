
from consts import *
from db_reader import SqlDatabase
from utils import setup_logging

from logging import getLogger; logger = getLogger(LOGGER_NAME)


def perform_logic_on_db(db):
    col_names = db.get_column_names()
    first_row = db.execute("select * from {} where id=1;".format(FLOW_TABLE))[0]

    logger.info("Source IP={}, Destination IP={}".format(first_row[db.header_to_id('sa')],
                                                   first_row[db.header_to_id('da')]))


def main():
    setup_logging()
    logger.critical("Welcome to the SSH Detector!")
    db = SqlDatabase(DB_PATH, default_table=FLOW_TABLE)
    db.open()
    logger.debug("Opened DB")
    try:
        logger.debug("Doing stuff")
        perform_logic_on_db(db)
    finally:
        db.close()
        logger.debug("Closed DB")
    logger.critical("Code finished successfully :)")
    return 0


if __name__ == '__main__':
    main()
