import sqlite3
import os


class Database:
    def __init__(self, db_name):
        if db_name not in os.listdir('.'):
            self.db_init(db_name)
        self.db = sqlite3.connect(db_name)
        self.csr = self.db.cursor()
        self.closed = False
        
    @staticmethod
    def db_init(self, db_name='test.db'):
        db = sqlite3.connect(db_name)
        csr = db.cursor()
        csr.execute('''create table corp_info(
                corp_name text,
                addr text
            )''')
        db.commit()
        db.close()
        
    def write(self, corp, addr):
        if not self.closed:
            self.csr.execute(f'''insert into corp_info values(
                '{corp}', '{addr}'
                )''')
        else:
            print('数据库已关闭')
        
    def close(self):
        if self.closed:
            return
        self.db.commit()
        self.db.close()
        self.closed = True
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    