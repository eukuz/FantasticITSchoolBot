import string
import secrets
import sqlite3
from strings import connections


class KeyGen:
    @staticmethod
    def __generateNKeys(n,control):
        symbols = string.digits + string.ascii_letters
        keys = set()
        conn = sqlite3.connect(connections["SQLite"])
        cursor = conn.cursor()
        fullTableName = KeyGen.__decodeControl(control)
        while len(keys) != n:
            key = "".join(secrets.choice(symbols) for i in range(13))
            cursor.execute("SELECT Key FROM "+fullTableName+" where Key = '"+key+"'")
            if not cursor.fetchone():
                keys.add(key)
        conn.close()
        return keys
    def __decodeControl(control):
        if control == "STD":
            fullTableName = "Students"
        elif control == "TEA":
            fullTableName = "Teachers"
        elif control == "CUR":
            fullTableName = "Curators"
        elif control == "PAR":
            fullTableName = "Parents"
        elif control == "COU":
            fullTableName = "Courses"
        elif control == "GRO":
            fullTableName = "Groups"
        return fullTableName

    def __writeKeysToDB(keys,control):

        conn = sqlite3.connect(connections["SQLite"])
        cursor = conn.cursor()
        values =""
        for key in keys:
            values += "('"+key+"'),"
        cursor.execute("INSERT INTO "+KeyGen.__decodeControl(control)+" (Key) VALUES "+ values[:-1])
        conn.commit()
        conn.close()

    def __getKeys(n, control):
        keys = KeyGen.__generateNKeys(n,control)
        KeyGen.__writeKeysToDB(keys,control)
        for key in keys:
            key = control + key
        return keys

    def generateNKeysStudents(n):
        return KeyGen.__getKeys(n,"STD")

    def generateNKeysTeachers(n):
        return KeyGen.__getKeys(n,"TEA")

    def generateNKeysCurators(n):
        return KeyGen.__getKeys(n, "CUR")

    def generateNKeysParents(n):
        return KeyGen.__getKeys(n, "PAR")

    def generateNKeysCourses(n):
        return KeyGen.__getKeys(n, "COU")

    def generateNKeysGroups(n):
        return KeyGen.__getKeys(n, "GRO")


def main():

    print(KeyGen.generateNKeysStudents(3))




main()
