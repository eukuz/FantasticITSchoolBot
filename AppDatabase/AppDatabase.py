import sqlite3

class AppDB:
    @staticmethod
    def __init__():
        con = sqlite3.connect("ITSchoolBotDB")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS Students (student_id text, parent_id text, group_id text")
        con.commit()
        con.close()
