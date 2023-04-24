import sqlite3
from contextlib import closing

class DBManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.create_tables()
    
    def query(self, sql):
        with closing(sqlite3.connect(self.db_name)) as con, con, closing(con.cursor()) as cur:
            cur.execute(sql)
            return cur.fetchall()
    
    def connect(self):
        self.con = sqlite3.connect(self.db_name)
        self.cursor = self.con.cursor()
        return self.cursor

    def close(self):
        self.con.commit()
        self.con.close()
        self.cursor = None
        self.con = None

    def rowcount(self):
        if self.cursor is None:
            raise Exception('Tried to get row count without connecting first')
        return self.cursor.rowcount

    def execute(self, query):
        if self.cursor is None:
            raise Exception('Tried to execute query without connecting first')
        self.cursor.execute(query)

    def create_tables(self):
        self.query('PRAGMA encoding = \'UTF-8\';')

        self.query('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER NOT NULL UNIQUE,
                guild_id INTEGER NOT NULL,
                member_id INTEGER NOT NULL,
                member_name TEXT NOT NULL,
                points INT NOT NULL,
                PRIMARY KEY (id),
                UNIQUE(guild_id, member_id)
            )''')

        self.query('''
            CREATE TABLE IF NOT EXISTS adminroles (
                id INTEGER NOT NULL UNIQUE,
                guild_id INTEGER NOT NULL,
                role_id INTEGER NOT NULL,
                PRIMARY KEY (id)
            )''')