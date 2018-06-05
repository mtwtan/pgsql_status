import psycopg2
import ConfigParser

class PgDatabase():
    def __init__(self):
        Config = ConfigParser.ConfigParser()
        Config.read("app/config.ini")
        host=Config.get('database','host')
        dbname=Config.get('database', 'dbname')
        username=Config.get('database', 'username')
        password=Config.get('database', 'password')

        self.conn = psycopg2.connect(host=host,dbname=dbname,user=username,password=password)
        self.cur = self.conn.cursor()
    
    def query(self, query):
        self.cur.execute(query)
        rows = self.cur.fetchall()
        #response = ''
        my_list = []
        for row in rows:
           my_list.append(row[0])

        return my_list
    
    def close(self):
        self.cur.close()
        self.conn.close()

