import string
import secrets
import sqlite3
from strings import connections


class KeyGen:
    @staticmethod
    def __generateNKeys(n, tableName):
        symbols = string.digits + string.ascii_letters
        keys = set()
        conn = sqlite3.connect(connections["SQLite"])
        cursor = conn.cursor()
        while len(keys) != n:
            key = "".join(secrets.choice(symbols) for i in range(13))
            # cursor.execute("SELECT Key FROM " + tableName + " where Key = '" + key + "'")
            if not cursor.fetchone():
                keys.add(key)
        conn.close()
        return keys

    def __writeKeysToDB(keys, tableName):
        conn = sqlite3.connect(connections["SQLite"])
        cursor = conn.cursor()
        values = ""
        for key in keys:
            values += "('" + key + "'),"
        # cursor.execute("INSERT INTO " + tableName + " (Key) VALUES " + values[:-1])
        conn.commit()
        conn.close()

    def __getKeys(n, tableName):
        keys = KeyGen.__generateNKeys(n, tableName)
        KeyGen.__writeKeysToDB(keys, tableName)
        control = tableName[0:3].upper()
        controlsKeys = set()
        for key in keys:
            controlsKeys.add(control + key)
        return controlsKeys

    def generateNKeysStudents(n):
        return KeyGen.__getKeys(n, "Students")

    def generateNKeysTeachers(n):
        return KeyGen.__getKeys(n, "Teachers")

    def generateNKeysCurators(n):
        return KeyGen.__getKeys(n, "Curators")

    def generateNKeysParents(n):
        return KeyGen.__getKeys(n, "Parents")

    def generateNKeysCourses(n):
        return KeyGen.__getKeys(n, "Courses")

    def generateNKeysGroups(n):
        return KeyGen.__getKeys(n, "Groups")

    def generateNKeys(n, tableName):
        return KeyGen.__getKeys(n, tableName)


def main():
    print(KeyGen.generateNKeysStudents(3))
    print(KeyGen.generateNKeys(3, 'Teachers'))


# main()
