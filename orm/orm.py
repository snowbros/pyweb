import db
import logging

logger = logging.getLogger(__name__)
class ORM(object):
    def __init__(self):
        table_name =  self._table_name
        db._create_table(table_name)
        logger.info("TEST LOG")
        logger.warning("TEST LOG")
        # for f in self._fields:
            # pass
            #logic for adding column