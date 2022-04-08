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
        # self.conn = DB('postgres://lxfzdnbztxpxsz:130b2f28cbc992e7154427e410aa96ca3337cecf7318fd451df86ab0f187bdfc@ec2-34-247-172-149.eu-west-1.compute.amazonaws.com:5432/d22lk9onn5sn1u')
        # self.conn.connect()
        # print('connection ok')


    async def create(self):
        await self.conn.connect()
        await self.conn.execute(sql.table1)
        await self.conn.execute(sql.table2)

    async def update_filters(self, values):
        """Run SQL query to update rows in table"""
        # self.connect()
        await self.conn.execute(sql.query_update_filters, values=values)


    async def subscriber_exists(self, values):
        """Run SQL query to check exists user"""
        # self.connect()
        record = await self.conn.fetch_one(sql.query_exists, values=values)
        return record

    async def add_subscriber(self, values):
        """Run SQL query to check exists user"""
        # self.connect()
        await self.conn.execute(sql.query_add, values=values)


    async def update_subscription(self, values):
        """Run SQL query to check exists user"""
        # self.connect()
        await self.conn.execute(sql.query_update, values=values)


    async def add_filters(self, values):
        """Run SQL query to add filter"""
        record = await self.conn.fetch_one(sql.query_person, values={'uid': values.get('uid')})
        if not record:
            return
        flag = await self.conn.fetch_one(sql.query_exist_filter,values={"user_id": record[0]})
        if flag:
            await self.conn.execute(sql.query_filter_update, values={'query_post':values.get('query_post'), 'user_id':record[0]})
        else:
            await self.conn.execute(sql.query_filter, values={'query_post':values.get('query_post'), 'user_id':record[0]})

    async def get_all_query(self):
        # self.connect()
        record = await self.conn.fetch_all(sql.query_get_filters)
        return record


if __name__ == '__main__':
    db = Database()
    values = {'uid':838019137, 'query_post': 'https'}
    asyncio.run(db.add_filters(values))
