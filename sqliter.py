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
        # # self.conn = DB(config.DB_URL)
        # self.conn = DB('postgresql://spoon:spoon@127.0.0.1:5432/project')
        self.conn = DB(config.DB_URL)
        # self.conn.connect()
        # self.conn = DB('postgres://fdhorobeymcpbn:d5c20ca6f5e9d72877d001f43678f0a0cea915cf5493347a4ff454d23022ebc3@ec2-63-32-248-14.eu-west-1.compute.amazonaws.com:5432/db9ob7a7v7mqhc')
        # print('connection ok')

    def update_filters(self, values):
        """Run SQL query to update rows in table"""
        # self.connect()
        self.conn.execute(sql.query_update_filters, values=values)


    async def subscriber_exists(self, values):
        """Run SQL query to check exists user"""
        # self.connect()
        record = await self.conn.fetch_all(sql.query_exists, values=values)
        return record

    async def add_subscriber(self, values):
        """Run SQL query to check exists user"""
        # self.connect()
        await self.conn.execute(sql.query_add, values=values)
        return True

    async def update_subscription(self, values):
        """Run SQL query to check exists user"""
        # self.connect()
        await self.conn.execute(sql.query_update, values=values)


    def add_filters(self, olx_query, user_uid):
        """Run SQL query to add filter"""
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

    async def get_all_query(self):
        # self.connect()
        record = await self.conn.fetch_all(sql.query_get_filters)
        return record


if __name__ == '__main__':
    db = Database()
    asyncio.run(db.connect())
