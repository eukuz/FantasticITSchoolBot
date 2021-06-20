from db.models import *
from peewee import *

class Database:
    def __init__(self):
        self._db = db
        self._db.connect()
        self._db.create_tables([Teachers, Parents, Tutors, Students, Homework, Groups])
        self._db.close()

def main():
    app_db = Database()

main()