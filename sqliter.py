import psycopg2
from psycopg2.extras import RealDictCursor

import config
import sql
import asyncio
import logging
logging.basicConfig(level=logging.INFO)
from databases import Database as DB

database = DB('postgresql:spoon:spoon//127.0.0.1/project',)




class Database:
    def __init__(self):
        # self.conn = DB(config.DB_URL)
        # self.conn = DB('postgresql://spoon:spoon@127.0.0.1:5432/project')
        self.conn = DB('postgres://fdhorobeymcpbn:d5c20ca6f5e9d72877d001f43678f0a0cea915cf5493347a4ff454d23022ebc3@ec2-63-32-248-14.eu-west-1.compute.amazonaws.com:5432/db9ob7a7v7mqhc')
        print('connection ok')

    async def connect(self):
        await self.conn.connect()
    async def last_post(self, vars=None):
        """Run SQL query to select rows from table"""
        record1 = await self.conn.execute(sql.table1)
        record2 = await self.conn.execute(sql.table2)


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
        with self.conn.cursor(cursor_factory=RealDictCursor) as curs:
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
        with self.conn.cursor() as cur:
            cur.execute(sql.query_update_filters, (simple, uid))
            self.conn.commit()
            cur.close()
            return f"{cur.rowcount} rows affected"

    def subscriber_exists(self, user_uid):
        """Run SQL query to check exists user"""
        self.connect()
        with self.conn.cursor() as curs:
            curs.execute(sql.query_exists, (user_uid,))
            record = curs.fetchone()
        return record

    def add_subscriber(self, user_uid, status):
        """Run SQL query to check exists user"""
        self.connect()
        with self.conn.cursor() as curs:
            curs.execute(sql.query_add, (user_uid, status))
            self.conn.commit()
            curs.close()
        return True

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
        with self.conn.cursor() as curs:
            curs.execute("SELECT id FROM subscribers WHERE personal_uid=%s", (user_uid, ))
            id = curs.fetchone()
            curs.execute('SELECT * FROM filters WHERE user_id=%s', id)
            exists_filter = curs.fetchone()
            if exists_filter:
                curs.execute(sql.query_filter_update, (olx_query, id[0]))
            else:
                curs.execute(sql.query_filter, (olx_query, id))
            self.conn.commit()
            curs.close()

    def get_all_query(self):
        self.connect()
        with self.conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute(sql.query_get_filters)
            record = curs.fetchall()
        return record

    def close(self):
        self.conn.close()

if __name__ == '__main__':
    db = Database()
    asyncio.run(db.connect())
