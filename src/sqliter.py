import sqlite3
import sql
import logging
import config
LOGGER = logging.getLogger(__name__)

class Database:
    def __init__(self, config):
        self.dbname = config.DATABASE_NAME
        self.conn = None

    def connect(self):
        """Connect to a postgres database"""
        if not self.conn:
            try:
                self.conn = sqlite3.connect(self.dbname)
            except sqlite3.DatabaseError as e:
                LOGGER.error(e)
                raise e
            finally:
                # self.conn.execute(sql.up)
                # self.conn.execute(sql.up1)
                LOGGER.info('Connection opened successfully')

    def last_post(self, vars=None):
        """Run SQL query to select rows from table"""
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(sql.query_url, vars=vars)
            record = cur.fetchone()
            cur.close()
            return record

    def inset_post(self):
        """Run SQL query to select rows from table"""
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(sql.query_insert, (10, 'https://4545', 'simple'))
            self.conn.commit()
            print(cur)
            cur.close()


    def select_row_dict(self, query):
        self.connect()
        with self.conn.cursor() as curs:
            curs.execute(query)
            record = curs.fetchall()
        return record

    def update_rows(self, query):
        """Run SQL query to update rows in table"""
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(query)
            self.conn.commit()
            cur.close()
            return f"{cur.rowcount} rows affected"

    def update_filters(self, simple,uid):
        """Run SQL query to update rows in table"""
        self.connect()
        curs = self.conn.cursor()
        curs.execute(sql.query_update_filters, (simple, uid))
        self.conn.commit()
        curs.close()
        return f"{curs.rowcount} rows affected"

    def subscriber_exists(self, user_uid):
        """Run SQL query to check exists user"""
        self.connect()
        self.conn.row_factory = sqlite3.Row
        curs = self.conn.cursor()
        curs.execute(sql.query_exists, (user_uid, ))
        record = curs.fetchone()
        return record

    def add_subscriber(self, user_uid, status):
        """Run SQL query to check exists user"""
        self.connect()
        self.conn.row_factory = sqlite3.Row
        curs = self.conn.cursor()
        curs.execute(sql.query_add, (user_uid, status))
        self.conn.commit()
        curs.close()

    def update_subscription(self, user_uid, status):
        """Run SQL query to check exists user"""
        self.connect()
        with self.conn.cursor() as curs:
            curs.execute(sql.query_update, (status, user_uid))
            self.conn.commit()
            curs.close()
        return True


    def add_filters(self, olx_query, user_uid):
        """Run SQL query to add filter"""
        self.connect()
        self.conn.row_factory = sqlite3.Row
        curs = self.conn.cursor()
        curs.execute("SELECT id FROM subscribers WHERE personal_uid=?", (user_uid, ))
        id = curs.fetchone()
        curs.execute('SELECT * FROM filters WHERE user_id=?', (id[0], ))
        exists_filter = curs.fetchone()
        if exists_filter:
            curs.execute(sql.query_filter_update, (olx_query, id[0]))
        else:
            curs.execute(sql.query_filter, (olx_query, id[0]))
        self.conn.commit()
        curs.close()

    def get_all_query(self):
        self.connect()
        self.conn.row_factory = sqlite3.Row
        curs = self.conn.cursor()
        curs.execute(sql.query_get_filters)
        record = curs.fetchall()
        return record

    def close(self):
        self.conn.close()

if __name__ == '__main__':
    db = Database(config)
    db.connect()